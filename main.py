import requests
import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch import Elasticsearch

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import psycopg2
import asyncio
import json 

firebase_config_path = 'firebase_config.json'

cred = credentials.Certificate(firebase_config_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

from price.KrxPriceModel import *

today = datetime.date.today()

target_date = today
limit = datetime.date(1995, 5, 3)

url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

def download_stock(target_date: datetime.date):
    target_date_str = target_date.strftime("%Y%m%d")
    data = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501', 'mktId': 'ALL', 'trdDd' : target_date_str, 'share' : '1', 'money': '1', "csvxls_isNo": "false"}
    req = requests.post(url, data=data)
    body = req.json()['OutBlock_1']
    temp_list = []
    if body[0]['TDD_CLSPRC'] != '-':
        for r in body:
            if r['TDD_CLSPRC'] != '-':
                temp_list.append(KrxStockPrice(target_date_str, r['ISU_SRT_CD'],r['ISU_ABBRV'],r['MKT_NM'],r['SECT_TP_NM'],r['TDD_CLSPRC'],r['CMPPREVDD_PRC'],r['FLUC_RT'],r['TDD_OPNPRC'],r['TDD_HGPRC'],r['TDD_LWPRC'],r['ACC_TRDVOL'],r['ACC_TRDVAL'],r['MKTCAP'],r['LIST_SHRS']))
    return temp_list

def download_etf(target_date: datetime.date):
    target_date_str = target_date.strftime("%Y%m%d")
    data = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT04301', 'trdDd' : target_date_str, 'share' : '1', 'money': '1', "csvxls_isNo": "false"}
    req = requests.post(url, data=data)
    body = req.json()['output']
    temp_list = []
    if body[0]['TDD_CLSPRC'] != '-':
        for r in body:
            if r['TDD_CLSPRC'] != '-':
                temp_list.append(KrxEtfPrice(target_date_str, r['ISU_SRT_CD'], r['ISU_ABBRV'], r['TDD_CLSPRC'], r['CMPPREVDD_PRC'], r['FLUC_RT'], r['NAV'], r['TDD_OPNPRC'], r['TDD_HGPRC'], r['TDD_LWPRC'], r['ACC_TRDVOL'], r['ACC_TRDVAL'], r['MKTCAP'], r['INVSTASST_NETASST_TOTAMT'], r['LIST_SHRS'], r['IDX_IND_NM'], r['OBJ_STKPRC_IDX'], r['CMPPREVDD_IDX'], r['FLUC_RT1']))
    return temp_list
    

async def upload_to_firestore(rows: list, target_date: datetime.date):
    target_date_str = target_date.strftime("%Y%m%d")
    #Group 500 each
    split_count = 0
    row_list = []
    while len(rows) > 500:
        split_count += 1
        row_list.append(rows[:500])
        rows = rows[500:]
    row_list.append(rows)

    doc_ref = db.collection("stock").document("price").collection(target_date_str)

    batch = db.batch()

    for group in row_list:
        for r in group:
            res = r.to_dict()
            batch.set(doc_ref.document(res['isu']), res)
        batch.commit()
print("Downloading..")


async def save_stock_to_database(rows: list[KrxStockPrice], conn):    
    cur = conn.cursor()

    for r in rows:
        cur.execute(
f"""INSERT INTO "korean_stock" (id, date, isu, name, market, sector, end_price, change_price, change_rate, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, number_of_share)
VALUES ('{r.date +'-'+r.isu}', '{r.date}', '{r.isu}','{r.name}','{r.market}','{r.sector}',{r.end_price},{r.change_price},{r.change_rate},{r.start_price},{r.highest_price},{r.lowest_price},{r.trade_volume},{r.trade_amount},{r.market_cap},{r.number_of_share})
ON CONFLICT (id) DO NOTHING""")
    conn.commit()

async def save_eft_to_database(rows: list[KrxEtfPrice], conn):    
    cur = conn.cursor()

    for r in rows:
        cur.execute(
f"""INSERT INTO "korean_etf" (id, date, isu, name, end_price, change_price, change_rate, net_value, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, net_cap_value, number_of_share, base_index_name, base_index_end_point, base_index_change_point, base_index_change_rate)
VALUES ('{r.date +'-'+r.isu}', '{r.date}', '{r.isu}', '{r.name}', '{r.end_price}', '{r.change_price}', '{r.change_rate}', '{r.net_value}', '{r.start_price}', '{r.highest_price}', '{r.lowest_price}', '{r.trade_volume}', '{r.trade_amount}', '{r.market_cap}', '{r.net_cap_value}', '{r.number_of_share}', '{r.base_index_name}', '{r.base_index_end_point}', '{r.base_index_change_point}', '{r.base_index_change_rate}')
ON CONFLICT (id) DO NOTHING""")
    conn.commit()


async def donwload_stock_local(rows:list[KrxStockPrice]):
    if len(rows) != 0:
        with open('krx/stock/' + rows[0].date + '.json', 'w') as f:
            for r in rows:
                j = r.to_dict()
                json.dump(j, f, ensure_ascii=False)

async def donwload_etf_local(rows:list[KrxEtfPrice]):
    if len(rows) != 0:
        with open('krx/etf/' + rows[0].date + '.json', 'w') as f:
            json.dump([r.to_dict() for r in rows], f, ensure_ascii=False)


async def save_to_elasticsearch(rows: list, index:str, client):
    if len(rows) > 0:
        body = []
        for entry in rows:
            body.append({'index': {'_index': index, '_id' : entry.date +'-'+ entry.isu}})
            body.append(entry.to_dict())
        client.bulk(body=body)


# while limit < target_date:
#     print(target_date.strftime("%Y-%m-%d"))
#     upload_to_firestore(download(target_date), target_date)
#     target_date = target_date - datetime.timedelta(days=1)

async def daily_job(today: datetime, conn, es_client):
    print("Target date : {}".format(today.strftime("%Y-%m-%d")))

    stock_rows = download_stock(today)
    task1 = asyncio.create_task(save_stock_to_database(stock_rows, conn))
    task2 = asyncio.create_task(save_to_elasticsearch(stock_rows, 'stock', es_client))
    task3 = asyncio.create_task(donwload_stock_local(stock_rows))
    task4 = asyncio.create_task(upload_to_firestore(stock_rows, today))
    # if today > datetime.date(2002, 10, 13):
    etf_rows = download_etf(today)
    task5 = asyncio.create_task(save_eft_to_database(etf_rows, conn))
    task6 = asyncio.create_task(donwload_etf_local(etf_rows))
    task7 = asyncio.create_task(save_to_elasticsearch(etf_rows, 'etf', es_client))
    await task5
    await task6
    await task7
    await task1
    await task2
    await task3
    await task4

conn = psycopg2.connect(
    host="localhost",
    database="finance",
    user="admin",
    password="1234")

es_client = Elasticsearch(['localhost:9200'])

#Daily Job
asyncio.run(daily_job(today, conn, es_client))

# while limit <= target_date:
#     asyncio.run(daily_job(target_date, conn, es_client))
#     target_date = target_date - datetime.timedelta(days=1)

conn.close()
es_client.close()
print("Finished")