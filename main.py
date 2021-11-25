
import datetime
import asyncio
import sys, getopt

from price.model.KrxPriceModel import *
from price.client.ElasticSearchClient import *
from price.client.PostgreSQLClient import *
from price.client.FirebaseClient import * 
from price.client.LocalStorageClient import *
from price.Crawler import *
import configparser


def main(arg):
    conf = configparser.SafeConfigParser()
    conf.read('config.ini')
    conf.sections()

    opts, etc_args = getopt.getopt(arg[1:], "hi:c:", ["help","instance=","channel="])
    
    if "--local" in etc_args: local_storage = True 
    else: local_storage = None
    
    if "--postgres" in etc_args:
        pd_conf = conf['PostgreSQL']
        pg_client = PostgreSQL
        pg_conn = PostgreSQL.get_connection(host=pd_conf['host'], database=pd_conf['db'], user=pd_conf['user'], password=pd_conf['password'])
        
    else: 
        pg_client = None
        pg_conn = None

    if "--elasitcsearch" in etc_args: es_client = ElasticSearch().get_client([conf['ElasticSearch']])
    else: etc_args = None
    
    if "--firestore" in etc_args: firestore_client = Firebase().getClient()
    else: firestore_client = None
    
    today = datetime.date.today()
    target_date = today
    for (opt, argument) in opts:
        if "--target-date" == opt:
            target_date = datetime.datetime.fromisoformat(argument)
        elif "--from" == opt:
            target_date = datetime.datetime.fromisoformat(argument)
        elif "--to" == opt:
            limit = datetime.datetime.fromisoformat(argument)

    try:
        if target_date == today:
            asyncio.run(daily_job(target_date, local_storage, firestore_client, es_client, pg_client, pg_conn))
        else:
            asyncio.run(run_in_range(target_date, limit, local_storage, firestore_client, es_client, pg_client, pg_conn))
    except Exception as e:
        print(f"Error %{e}")
    finally:
        if pg_conn != None: pg_conn.close()
        if es_client != None: es_client.close()

if __name__ == '__main__':
    main(sys.argv)


async def run_in_range(from_date: datetime, to_date:datetime, local_storage, firestore_client, es_client, pg_client, pg_conn):
    target_date = from_date
    while target_date <= to_date:
        daily_job(target_date, local_storage, firestore_client, es_client, pg_client, pg_conn)
        target_date = target_date + datetime.timedelta(days=1)

async def daily_job(today: datetime, local_storage, firestore_client, es_client, pg_client, pg_conn):
    print("Target date : {}".format(today.strftime("%Y-%m-%d")))

    stock_rows = download_stock(today)
    if (pg_client != None): await asyncio.create_task(pg_client.save_stock_to_database(stock_rows, pg_conn))
    if (es_client != None): await asyncio.create_task(es_client.save_to_elasticsearch(stock_rows, 'stock', es_client))
    if (local_storage != None): await asyncio.create_task(local_storage.donwload_stock_local(stock_rows, 'krx/stock'))
    if(firestore_client != None): await asyncio.create_task(firestore_client.upload_to_firestore(stock_rows, today))

    etf_rows = download_etf(today)
    if(pg_client != None): await asyncio.create_task(pg_client.save_eft_to_database(etf_rows, pg_conn))
    if(es_client != None): await asyncio.create_task(es_client.save_to_elasticsearch(etf_rows, 'etf', es_client))
    if(local_storage != None): await asyncio.create_task(local_storage.donwload_etf_local(etf_rows, 'krx/etf'))