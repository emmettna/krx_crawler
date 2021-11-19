class KrxStockPrice:

    def __init__(self, date, isu, name, market, sector, end_price, change_price, change_rate, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, number_of_share):
        self.isu = isu
        self.name = name
        self.date = date
        self.market = market
        self.sector = sector
        self.end_price = int(end_price.replace(",", ""))
        self.change_price = int(change_price.replace(",", ""))
        self.change_rate = float(change_rate.replace(",", ""))
        self.start_price = int(start_price.replace(",", ""))
        self.highest_price = int(highest_price.replace(",", ""))
        self.lowest_price = int(lowest_price.replace(",", ""))
        self.trade_volume = int(trade_volume.replace(",", ""))
        self.trade_amount = int(trade_amount.replace(",", ""))
        self.market_cap = int(market_cap.replace(",", ""))
        self.number_of_share = int(number_of_share.replace(",", ""))
    def __str__(self):
        return f"""KrxStockPrice(date: {self.date}, isu: {self.isu}, name: {self.name}, market: {self.market}, \
sector: {self.sector}, end_price: {self.end_price}, change_price: {self.change_price}, change_rate: {self.change_rate}, start_price: {self.start_price}, \
highest_price: {self.highest_price}, lowest_price: {self.lowest_price}, trade_volume: {self.trade_volume}, trade_amount: {self.trade_amount}, \
market_cap: {self.market_cap}, number_of_share: {self.number_of_share})"""
    def __getitems__(self):
        return [self.date, self.isu, self.name, self.market, self.sector, self.end_price, self.start_price, self.highest_price, self.lowest_price, 
        self.trade_volume, self.trade_amount, self.market_cap, self.number_of_share]
    def to_dict(self):
        return {'date': self.date, 'isu': self.isu,'name': self.name,'market': self.market,'sector': self.sector,'end_price': self.end_price,'change_price': self.change_price,'change_rate': self.change_rate,'start_price': self.start_price,'highest_price': self.highest_price,'lowest_price': self.lowest_price,'trade_volume': self.trade_volume,'trade_amount': self.trade_amount,'market_cap': self.market_cap,'number_of_share': self.number_of_share}