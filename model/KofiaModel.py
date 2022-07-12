class KofiaStockLoanHistory:
    def __init__(self, date, name, market, code, traded_volume, returned_volume, left_stock_volume, left_stock_price):
        self.date = date #날짜
        self.name = name.strip() #종목명
        self.market = market #마켓
        self.code = code.strip() #종목코드
        self.traded_volume = int(traded_volume) #채결(주수)
        self.returned_volume = int(returned_volume) #상환(주수)
        self.left_stock_volume = int(left_stock_volume) #잔고 주수
        self.left_stock_price = int(left_stock_price) # 잔고 금액(백만원)
    def __str__(self) -> str:
        return f"""Lazy..."""
    
    def __getitems__(self):
        return [self.date, self.name, self.market, self.code, self.traded_volume, self.returned_volume, self.left_stock_volume, self.left_stock_price]

    def get_unique_id(self )-> str: return self.date.strftime("%Y-%m-%d") +'-'+ self.code

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"), 
            'name': self.name, 
            'market':self.market, 
            'code': self.code, 
            'traded_volume': self.traded_volume, 
            'returned_volume' : self.returned_volume, 
            'left_stock_volume' : self.left_stock_volume, 
            'left_stock_price' : self.left_stock_price
            }

class KofiaMarketCapitalFlowHistory:
    def __init__(self, date, deposit, deriviation_deposit, RP, entrust_outstanding, entrust_liquidation_outstanding, liquidation_rate):
        self.date = date #날짜
        self.deposit = int(deposit) #투자자예탁금(장내파생상품 거래예수금제외)
        self.deriviation_deposit = int(deriviation_deposit) #장내파생상품 거래 예수금
        self.RP = int(RP) #대고객 환매 조건부 채권
        self.entrust_outstanding = int(entrust_outstanding) #위탁매매 미수금
        self.entrust_liquidation_outstanding = int(entrust_liquidation_outstanding) #위탁매매 미수금 대비 실제 반대매매금
        self.liquidation_rate = float(liquidation_rate) #미수금 대비 반대매매비중(%)

    def __str__(self) -> str:
        return f"""Lazy..."""

    def get_unique_id(self )-> str: return self.date.strftime("%Y-%m-%d")
    
    def __getitems__(self):
        return [self.date, self.deposit, self.deriviation_deposit, self.RP, self.entrust_outstanding, self.entrust_liquidation_outstanding, self.liquidation_rate]

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"), 
            'deposit': self.deposit, 
            'deriviation_deposit':self.deriviation_deposit, 
            'RP': self.RP, 
            'entrust_outstanding': self.entrust_outstanding, 
            'entrust_liquidation_outstanding' : self.entrust_liquidation_outstanding, 
            'liquidation_rate' : self.liquidation_rate,
            }

class KofiaKoreaBondHistory:
    def __init__(self, date, name, period, morning_rate, afternoon_rate, change_rate, previous_day_rate, highest_of_year_rate, lowest_of_year_rate):
        def nullToZero(value): return float(0) if value is None else float(value)

        self.date = date #날짜
        self.name = name.strip() #종류명
        self.period = period.strip() #기간
        self.morning_rate = nullToZero(morning_rate) #당일 오전
        self.afternoon_rate = nullToZero(afternoon_rate) #당일 오후
        self.change_rate = nullToZero(change_rate) #전일대비
        self.previous_day_rate = nullToZero(previous_day_rate) #전일
        self.highest_of_year_rate = nullToZero(highest_of_year_rate) #연중최고
        self.lowest_of_year_rate = nullToZero(lowest_of_year_rate) #연중최저

    def __str__(self) -> str:
        return f"""Lazy..."""

    def get_unique_id(self )-> str: return self.date.strftime("%Y-%m-%d") +'-'+ self.name
    
    def __getitems__(self):
        return [self.date, self.name, self.period, self.morning_rate, self.afternoon_rate, self.change_rate, self.previous_day_rate, self.highest_of_year_rate, self.lowest_of_year_rate]

    def to_dict(self):
        return {
            'date': self.date.strftime("%Y-%m-%d"), 
            'name': self.name,
            'period': self.period,
            'morning_rate': self.morning_rate, 
            'afternoon_rate':self.afternoon_rate, 
            'change_rate': self.change_rate, 
            'previous_day_rate': self.previous_day_rate, 
            'highest_of_year_rate' : self.highest_of_year_rate, 
            'lowest_of_year_rate' : self.lowest_of_year_rate,
            }