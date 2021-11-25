import datetime
import requests
from model.KrxPriceModel import *

url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

def download_stock(target_date: datetime.date) -> list:
    if(target_date >= datetime.date(1995, 5, 2)):
        target_date_str = target_date.strftime("%Y%m%d")
        payload = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501', 'mktId': 'ALL', 'trdDd' : target_date_str, 'share' : '1', 'money': '1', "csvxls_isNo": "false"}
        req = requests.post(url, data=payload)
        body = req.json()['OutBlock_1']
        temp_list = []
        if body[0]['TDD_CLSPRC'] != '-':
            for r in body:
                if r['TDD_CLSPRC'] != '-':
                    temp_list.append(KrxStockPrice(target_date, r['ISU_SRT_CD'],r['ISU_ABBRV'],r['MKT_NM'],r['SECT_TP_NM'],r['TDD_CLSPRC'],r['CMPPREVDD_PRC'],r['FLUC_RT'],r['TDD_OPNPRC'],r['TDD_HGPRC'],r['TDD_LWPRC'],r['ACC_TRDVOL'],r['ACC_TRDVAL'],r['MKTCAP'],r['LIST_SHRS']))
        return temp_list
    else:
        print("[Info] Krx stock data is from 1995-May-2")
        return []

def download_etf(target_date: datetime.date) -> list:
    if (target_date >= datetime.date(2002, 10, 13) ):
        target_date_str = target_date.strftime("%Y%m%d")
        payload = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT04301', 'trdDd' : target_date_str, 'share' : '1', 'money': '1', "csvxls_isNo": "false"}
        req = requests.post(url, data=payload)
        body = req.json()['output']
        temp_list = []
        if body[0]['TDD_CLSPRC'] != '-':
            for r in body:
                if r['TDD_CLSPRC'] != '-':
                    temp_list.append(KrxEtfPrice(target_date, r['ISU_SRT_CD'], r['ISU_ABBRV'], r['TDD_CLSPRC'], r['CMPPREVDD_PRC'], r['FLUC_RT'], r['NAV'], r['TDD_OPNPRC'], r['TDD_HGPRC'], r['TDD_LWPRC'], r['ACC_TRDVOL'], r['ACC_TRDVAL'], r['MKTCAP'], r['INVSTASST_NETASST_TOTAMT'], r['LIST_SHRS'], r['IDX_IND_NM'], r['OBJ_STKPRC_IDX'], r['CMPPREVDD_IDX'], r['FLUC_RT1']))
        return temp_list
    else:
        print("[Info] Krx ETF data is from 2002-October-13")
        return []