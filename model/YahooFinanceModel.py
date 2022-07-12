import datetime

class YahooFinanceRow:
    def __init__(self, timestamp, name, symbol, low, open, volume, high, close):
        def nullToZero(value): return float(0) if value is None else float(value)
        date = datetime.datetime.fromtimestamp(timestamp)
        self.date = date #날짜
        self.name = name.strip() #종목명
        self.symbol = symbol.strip() #symbol
        self.open = nullToZero(open) #시가
        self.volume = nullToZero(volume) #거래량
        self.high = nullToZero(high) #최고가
        self.close = nullToZero(close) #종가
        self.low = nullToZero(low) #최저가

    def __str__(self) -> str:
        return f"""YahooFinanceRow(date: {self.date}, name: {self.name}, symbol: {self.symbol}, open: {self.open}, close: {self.close}, high: {self.high}, low: {self.low}, volume: {self.volume})"""

    def get_unique_id(self )-> str: return self.date.strftime("%Y-%m-%d") +'-'+ self.name
    
    def __getitems__(self):
        return [self.date, self.name, self.symbol, self.open, self.volume, self.high, self.close, self.low]

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"), 
            'name': self.name,
            'symbol': self.symbol,
            'open': self.open,
            'volume': self.volume, 
            'high':self.high, 
            'close': self.close, 
            'low': self.low,
            }