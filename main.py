import datetime
import asyncio

from model.KrxPriceModel import *
from client.ElasticSearchClient import *
from client.PostgreSQLClient import *
from client.FirestoreClient import * 
from client.LocalStorageClient import *
from Crawler import *
import configparser
import argparse

def main():
    today = datetime.date.today()

    conf = configparser.ConfigParser()
    conf.read('config.ini')
    conf.sections()

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument('--all', type=str, nargs="?", const=True, default=False)
    argumentParser.add_argument('--local', type=str, nargs="?", const=True, default=False)
    argumentParser.add_argument('--postgres', type=str, nargs="?", const=True, default=False)
    argumentParser.add_argument('--elasticsearch', type=str,  nargs="?", const=True, default=False)
    argumentParser.add_argument('--firestore', type=str, nargs="?", const=True, default=False)
    argumentParser.add_argument('--target_date', type=str)
    argumentParser.add_argument('--start_date', type=str)
    argumentParser.add_argument('--end_date', type=str)
    args = argumentParser.parse_args()

    if args.all | (not (args.local | args.postgres | args.elasticsearch | args.firestore)):
        args.postgres = True
        args.elasticsearch = True
        args.firestore = True
        args.local = True

    if args.local: 
        local_download_parent_dir=conf['LocalDownload']['parent_dir']
        local_storage = True 
    else: local_storage = False

    if args.postgres:
        pd_conf = conf['PostgreSQL']
        pg_client = PostgreSQL
        pg_conn = PostgreSQL.get_connection(host=pd_conf['host'], port=pd_conf['port'], database=pd_conf['db'], user=pd_conf['user'], password=pd_conf['password'])
    else: 
        pg_client = None
        pg_conn = None

    if args.elasticsearch:
        es_client = ElasticSearch.get_client([conf['ElasticSearch']['host']])
    else: es_client = None
    
    if args.firestore: 
        import json 
        f = open('firebase_config.json')
        firebase_config = json.load(f)
        f.close()
        firestore_client = Firestore.getClient(firebase_config)
    else: firestore_client = None
    
    target_date = today
    limit = None
    
    if args.target_date != None:
        target_date = datetime.datetime.fromisoformat(args.target_date).date()
    elif args.start_date is not None:
        target_date = datetime.datetime.fromisoformat(args.start_date).date()
    if args.end_date is not None:
        limit = datetime.datetime.fromisoformat(args.end_date).date()

    async def run_in_range(start_date: datetime, end_date: datetime, local_storage, firestore_client, es_client, pg_client, pg_conn):
        target_date = start_date
        while target_date <= end_date:
            await daily_job(target_date, local_storage, firestore_client, es_client, pg_client, pg_conn)
            target_date = target_date + datetime.timedelta(days=1)

    async def daily_job(today: datetime, local_storage, firestore_client, es_client: ElasticSearch, pg_client: PostgreSQL, pg_conn):
        print("Target date : {}".format(today.strftime("%Y-%m-%d")))

        stock_rows = download_stock(today)
        if (pg_client != None): await asyncio.create_task(pg_client.save_stock(stock_rows, pg_conn))
        if (es_client != None): await asyncio.create_task(ElasticSearch.save(stock_rows, 'stock', es_client))
        if (local_storage): await asyncio.create_task(save(stock_rows, local_download_parent_dir + '/stock'))
        if(firestore_client != None): await asyncio.create_task(Firestore.upload_to_firestore(stock_rows, today, firestore_client))
        
        stock_base_values_rows = download_stock_base_values(today)
        if(sum((row.end_price for row in stock_base_values_rows)) > 0):
            if (pg_client != None): await asyncio.create_task(pg_client.save_stock_base_values(stock_base_values_rows, pg_conn))
            if (pg_client != None): await asyncio.create_task(pg_client.save_stock_base_value_avg(pg_conn, today))
            if (pg_client != None): await asyncio.create_task(pg_client.upsert_under_valued_assets_to_cache(pg_conn, today))
            if (es_client != None): await asyncio.create_task(ElasticSearch.save(stock_base_values_rows, 'stock_values', es_client))
            if (local_storage): await asyncio.create_task(save(stock_base_values_rows, local_download_parent_dir + '/stock_values'))

        etf_rows = download_etf(today)
        if(pg_client != None): await asyncio.create_task(pg_client.save_eft(etf_rows, pg_conn))
        if(es_client != None): await asyncio.create_task(ElasticSearch.save(etf_rows, 'etf', es_client))
        if(local_storage): await asyncio.create_task(save(etf_rows, local_download_parent_dir + '/etf'))

    try:
        if limit != None:
            asyncio.run(run_in_range(target_date, limit, local_storage, firestore_client, es_client, pg_client, pg_conn))
        else:
            asyncio.run(daily_job(target_date, local_storage, firestore_client, es_client, pg_client, pg_conn))
    except Exception as e:
        print(f"Error %{e}")
    finally:
        if pg_conn != None: pg_conn.close()
        if es_client != None: es_client.close()

if __name__ == '__main__':
    main()
    print("Done")