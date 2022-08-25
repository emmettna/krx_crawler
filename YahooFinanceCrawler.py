import datetime
from email.headerregistry import ContentTypeHeader
from re import template
import requests
from model.YahooFinanceModel import *

def base_url(symbol, start_time, end_time):
    return "https://query1.finance.yahoo.com/v8/finance/chart/{}&period1={}&period2={}&useYfid=true&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=w80is1V.ptB&corsDomain=finance.yahoo.com".format(symbol, str(int(start_time)), str(int(end_time)))

WTI_symbol = "CL=F?symbol=CL%3DF"
gold_symbol = "GC=F?symbol=GC%3DF"
copper_symbol = "HG=F?symbol=HG%3DF"

snp_ticker = "%5EGSPC?symbol=%5EGSPC"
nasdaq_ticker = "%5EIXIC?symbol=%5EIXIC"
kospi_ticker = "%5EKS11?symbol=%5EKS11"
kosdaq_ticker = "%5EKQ11?symbol=%5EKQ11"
vix_ticker = "%5EVIX?symbol=%5EVIX"

euro_ticker = "EUR=X?symbol=EUR%3DX"
cad_ticker = "CAD=X?symbol=CAD%3DX"
krw_ticker = "KRW=X?symbol=KRW%3DX"

def download_commodity(target_date: datetime.datetime) -> list:
    gold_rows = download_asset(target_date, "Gold", gold_symbol)
    copper_rows = download_asset(target_date, "Copper", copper_symbol)
    wti_rows = download_asset(target_date, "Crude Oil WTI", WTI_symbol)
    return gold_rows + wti_rows + copper_rows

def download_index(target_date: datetime.date) -> list:
    snp_rows = download_asset(target_date, "S&P 500", snp_ticker)
    nasdaq_rows = download_asset(target_date, "Nasdaq", nasdaq_ticker)
    kospi_rows = download_asset(target_date, "Kospi", kospi_ticker)
    kosdaq_rows = download_asset(target_date, "Kosdaq", kosdaq_ticker)
    vix_rows = download_asset(target_date, "Vix", vix_ticker)
    return snp_rows + nasdaq_rows + kospi_rows + kosdaq_rows + vix_rows

def download_currency(target_date: datetime.date) -> list:
    euro_rows = download_asset(target_date, "USD/EURO", euro_ticker)
    cad_rows = download_asset(target_date, "USD/CAD", cad_ticker)
    krw_rows = download_asset(target_date, "USD/KRW", krw_ticker)
    return euro_rows + cad_rows + krw_rows

def download_asset(target_date: datetime.date, name, symbol) -> list:
    if(target_date >= datetime.date(1995, 5, 2)):
        target_date = datetime.datetime.combine(target_date, datetime.datetime.min.time())
        start_date_timestamp = target_date.timestamp()
        end_date_timestamp = (target_date + datetime.timedelta(days=1)).timestamp() - 1
        print(end_date_timestamp)
        try:
            req = requests.get(base_url(symbol, start_date_timestamp, end_date_timestamp), headers={'User-Agent': "".join(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/87.0.4280.66 "
        "Safari/537.36"
        )})
            result = req.json()['chart']['result'][0]
            if(str(result['indicators']['quote']) != '[{}]'):
                temp_list = []
                for (timestamp, low, open, volume, high, close) in zip(result['timestamp'], result['indicators']['quote'][0]['low'], result['indicators']['quote'][0]['open'], result['indicators']['quote'][0]['volume'], result['indicators']['quote'][0]['high'], result['indicators']['quote'][0]['close']):
                    temp_list.append(YahooFinanceRow(timestamp, name, result['meta']['symbol'], low, open, volume, high, close))
                return temp_list
            return []
        except Exception as e:
            print("Failed to downaload asset name:`{}`, symbol: `{}` ".format(name, symbol))
            print(e)
    else:
        print("[Info] Yahoo finance data is from 1995-May-2")
        return []