import requests
import datetime
from dateutil.relativedelta import relativedelta

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import psycopg2
import uuid
import asyncio
import json 

firebase_config_path = 'firebase_config.json'

cred = credentials.Certificate(firebase_config_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

from price.KrxStockPriceModel import KrxStockPrice

today = datetime.date.today()

# Start from 20211109
# target_date = datetime.date(2021, 11, 9)
target_date = datetime.date(2013, 9, 6)
limit = datetime.date(1995, 5, 2)
# limit = today - relativedelta(years=1)

url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

def download(target_date: datetime.date):
    target_date_str = target_date.strftime("%Y%m%d")
    data = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501', 'mktId': 'ALL', 'trdDd' : target_date_str, 'share' : '1', 'money': '1', "csvxls_isNo": "false"}
    req = requests.post(url, data=data)
    body = req.json()['OutBlock_1']
    if body[0]['TDD_CLSPRC'] != '-':
        return [KrxStockPrice(target_date_str, r['ISU_SRT_CD'],r['ISU_ABBRV'],r['MKT_NM'],r['SECT_TP_NM'],r['TDD_CLSPRC'],r['CMPPREVDD_PRC'],r['FLUC_RT'],r['TDD_OPNPRC'],r['TDD_HGPRC'],r['TDD_LWPRC'],r['ACC_TRDVOL'],r['ACC_TRDVAL'],r['MKTCAP'],r['LIST_SHRS']) for r in body]
    else:
        return []

def upload_to_firestore(rows: list, target_date: datetime.date):
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


async def save_to_storage(rows: list[KrxStockPrice], conn):    
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS "korean_stock"
(
    id                   UUID        PRIMARY KEY,
    date                 DATE        NOT NULL,
    isu                  TEXT        NOT NULL,
    name                 TEXT        NOT NULL,
    market               TEXT        NOT NULL,
    sector               TEXT        ,
    end_price            BIGINT      NOT NULL,
    change_price         BIGINT      NOT NULL,
    change_rate          REAL        NOT NULL,
    start_price          BIGINT      NOT NULL,
    highest_price        BIGINT      NOT NULL,
    lowest_price         BIGINT      NOT NULL,
    trade_volume         BIGINT      NOT NULL,
    trade_amount         BIGINT      NOT NULL,
    market_cap           BIGINT      NOT NULL,
    number_of_share      BIGINT      NOT NULL,
    updated_at           TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);""")
    conn.commit()

    for r in rows:
        cur.execute(
f"""INSERT INTO "korean_stock" (id, date, isu, name, market, sector, end_price, change_price, change_rate, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, number_of_share)
VALUES ('{uuid.uuid4()}', '{r.date}', '{r.isu}','{r.name}','{r.market}','{r.sector}',{r.end_price},{r.change_price},{r.change_rate},{r.start_price},{r.highest_price},{r.lowest_price},{r.trade_volume},{r.trade_amount},{r.market_cap},{r.number_of_share})""")
    conn.commit()
    try: 
        print(f"Saved date for {rows[0].date}")
    except:
        print("Faild to print")


async def donwload_local(rows:list[KrxStockPrice]):
    if len(rows) != 0:
        with open('krx/' + rows[0].date + '.json', 'w') as f:
            for r in rows:
                j = r.to_dict()

                json.dump(j, f, ensure_ascii=False)
    print("file_saved")


# while limit < target_date:
#     print(target_date.strftime("%Y-%m-%d"))
    # upload_to_firestore(download(target_date), target_date)
    # target_date = target_date - datetime.timedelta(days=1)
conn = psycopg2.connect(
    host="localhost",
    database="finance",
    user="admin",
    password="1234")

while limit < target_date:
    print(target_date.strftime("%Y-%m-%d"))
    rows = download(target_date)
    asyncio.run(save_to_storage(rows, conn))
    asyncio.run(donwload_local(rows))
    target_date = target_date - datetime.timedelta(days=1)


conn.close()
