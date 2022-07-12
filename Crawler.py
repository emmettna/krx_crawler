import datetime
from email.headerregistry import ContentTypeHeader
from re import template
import requests
from model.KrxPriceModel import *
from model.KofiaModel import *

url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
kofia_url = "http://freesis.kofia.or.kr/meta/getMetaDataList.do"


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


def download_stock_base_values(target_date: datetime.date)-> str:
    if(target_date >= datetime.date(2000, 1, 4)):
        target_date_str = target_date.strftime("%Y%m%d")
        payload = {'bld': 'dbms/MDC/STAT/standard/MDCSTAT03501', 'mktId': 'ALL', 'trdDd' : target_date_str, 'searchType' : '1', "csvxls_isNo": "false"}
        req = requests.post(url, data=payload)
        body = req.json()['output']
        temp_list = []
        for r in body:
            temp_list.append(KrxStockBaseValues(target_date, r['ISU_SRT_CD'],r['ISU_ABBRV'],r['TDD_CLSPRC'],r['EPS'],r['PER'],r['FWD_EPS'],r['FWD_PER'],r['BPS'],r['PBR'],r['DPS'],r['DVD_YLD']))
        return temp_list
    else:
        print("[Info] Krx stock data is from 2000-Jan-4")
        return []

def download_stock_loans(target_date: datetime.date) -> list:
    if(target_date >= datetime.date(2008,10,20)):
        target_date_str = target_date.strftime("%Y%m%d")
        kospi_payload = {'dmSearch': { "tmpV40": "1000000", "tmpV41": "1", "tmpV1": "D", "tmpV45": target_date_str, "tmpV46": "", "tmpV74": "1,0,,1", "OBJ_NM": "STATSCU0100000130BO" }}
        kosdaq_payload = {'dmSearch': { "tmpV40": "1000000", "tmpV41": "1", "tmpV1": "D", "tmpV45": target_date_str, "tmpV46": "", "tmpV74": "2,0,,1", "OBJ_NM": "STATSCU0100000130BO" }}
        kospi_req = requests.post(kofia_url, json=kospi_payload)
        kosdaq_req = requests.post(kofia_url, json=kosdaq_payload)
        kospi_body = kospi_req.json()['ds1']
        kosdaq_body = kosdaq_req.json()['ds1']
        temp_list = []
        for r2 in kosdaq_body:
            temp_list.append(KofiaStockLoanHistory(target_date, r2['TMPV1'], 'KOSDAQ', r2['TMPV2'], r2['TMPV3'], r2['TMPV4'], r2['TMPV5'], r2['TMPV6']))
        for r in kospi_body:
            temp_list.append(KofiaStockLoanHistory(target_date, r['TMPV1'], 'KOSPI', r['TMPV2'], r['TMPV3'], r['TMPV4'], r['TMPV5'], r['TMPV6']))
        return temp_list
    else:
        print("[Info] Kofia stockload data is from 2008-10-20")
        return []

def download_market_capital_flow(target_date: datetime.date) -> list:
    if(target_date >= datetime.date(2008,10,20)):
        target_date_str = target_date.strftime("%Y%m%d")
        payload = {"dmSearch": {"tmpV40": "1000000", "tmpV41": "1", "tmpV1": "D", "tmpV45": target_date_str, "tmpV46": target_date_str, "OBJ_NM": "STATSCU0100000060BO"}}
        req = requests.post(kofia_url, json=payload)
        body = req.json()['ds1']
        temp_list = []
        for r in body:
            temp_list.append(KofiaMarketCapitalFlowHistory(target_date, r['TMPV2'], r['TMPV3'], r['TMPV4'], r['TMPV5'], r['TMPV6'], r['TMPV7']))
        return temp_list
    else:
        print("[Info] Kofia market capital flow data is from 2008-10-20")
        return []

def download_korea_treasury_bond_history(target_date: datetime.date) -> list:
    if(target_date >= datetime.date(2008,10,20)):
        target_date_str = target_date.strftime("%Y%m%d")
        payload = {"dmSearch": { "tmpV40": "", "tmpV41": "", "tmpV1": "D", "tmpV45": target_date_str, "tmpV46": "", "OBJ_NM": "STATBND0100000010BO"}}
        req = requests.post(kofia_url, json=payload)
        body = req.json()['ds1']
        temp_list = []
        for r in body:
            temp_list.append(KofiaKoreaBondHistory(target_date, r['TMPV1'], r['TMPV2'], r['TMPV3'], r['TMPV4'], r['TMPV5'], r['TMPV6'], r['TMPV8'], r['TMPV9']))
        return temp_list
    else:
        print("[Info] Kofia treasury bond data is from 2008-10-20")
        return []