import requests
import datetime
from dateutil.relativedelta import relativedelta

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebase_config_path = 'firebase_config.json'

cred = credentials.Certificate(firebase_config_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

from price.KrxStockPriceModel import KrxStockPrice

today = datetime.date.today()

# Start from 20211109
target_date = datetime.date(2021, 11, 9)
limit = today - relativedelta(years=1)

url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

def download(target_date: datetime.date):
    target_date_str = target_date.strftime("%Y%m%d")
    data = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501', 'mktId': 'ALL', 'trdDd' : yesterday_str, 'share' : '1', 'money': '1', "csvxls_isNo": "false"}
    req = requests.post(url, data=data)
    body = req.json()['OutBlock_1']

    rows = [KrxStockPrice(r['ISU_SRT_CD'],r['ISU_ABBRV'],r['MKT_NM'],r['SECT_TP_NM'],r['TDD_CLSPRC'],r['CMPPREVDD_PRC'],r['FLUC_RT'],r['TDD_OPNPRC'],r['TDD_HGPRC'],r['TDD_LWPRC'],r['ACC_TRDVOL'],r['ACC_TRDVAL'],r['MKTCAP'],r['LIST_SHRS']) for r in body]

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

while limit < target_date:
    print(target_date.strftime("%Y-%m-%d"))
    download(target_date)
    target_date = target_date - datetime.timedelta(days=1)