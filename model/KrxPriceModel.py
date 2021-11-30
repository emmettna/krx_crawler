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
        return {'date': self.date.strftime("%Y-%m-%d"), 'isu': self.isu,'name': self.name,'market': self.market,'sector': self.sector,'end_price': self.end_price,'change_price': self.change_price,'change_rate': self.change_rate,'start_price': self.start_price,'highest_price': self.highest_price,'lowest_price': self.lowest_price,'trade_volume': self.trade_volume,'trade_amount': self.trade_amount,'market_cap': self.market_cap,'number_of_share': self.number_of_share}


class KrxStockBaseValues:
    def __init__(self, date, isu, name, end_price, eps, per, forward_eps, forward_per, bps, pbr, dps, dividen_yield) -> None:
        self.date = date
        self.isu = isu
        self.name = name
        self.end_price = int(end_price.replace(",", "").replace("-", "0"))
        self.eps = int(eps.replace(",", "").replace("-", "0"))
        self.per = float(per.replace(",", "").replace("-", "0"))
        self.forward_eps = float(forward_eps.replace(",", "").replace("-", "0"))
        self.forward_per = float(forward_per.replace(",", "").replace("-", "0"))
        self.bps = int(bps.replace(",", "").replace("-", "0"))
        self.pbr = float(pbr.replace(",", "").replace("-", "0"))
        self.dps = int(dps.replace(",", "").replace("-", "0"))
        self.dividen_yield = float(dividen_yield.replace(",", "").replace("-", "0"))
    def get_unique_id(self )-> str: return self.date.strftime("%Y-%m-%d") +'-'+ self.isu
    def __str__(self) -> str:
        return f"""KrxStockBaseValue('date':{self.date},'isu':{self.isu},'name':{self.name},'end_price':{self.end_price},'eps':{self.eps},'per':{self.per},'forward_eps':{self.forward_eps},'forward_per':{self.forward_per},'bps':{self.bps},'pbr':{self.pbr},'dps':{self.dps},'dividen_yield':{self.dividen_yield})"""
    def to_dict(self):
        return {'date' :self.date.strftime("%Y-%m-%d"),'isu' :self.isu,'name' :self.name,'end_price' :self.end_price,'eps' :self.eps,'per' :self.per,'forward_eps' :self.forward_eps,'forward_per' :self.forward_per,'bps' :self.bps,'pbr' :self.pbr,'dps' :self.dps,'dividen_yield' :self.dividen_yield}

class KrxEtfPrice:
    def __init__(self, date, isu, name, end_price, change_price, change_rate, net_value, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, net_cap_value, number_of_share, base_index_name, base_index_end_point, base_index_change_point, base_index_change_rate):
        self.isu = isu
        self.date = date
        self.name = name
        self.end_price = int(end_price.replace(",", ""))
        self.change_price = int(change_price.replace(",", "")) if change_price != '-' else 0
        self.change_rate = float(change_rate.replace(",", "")) if change_rate != '-' else float("0.00")
        self.net_value = float(net_value.replace(",", ""))
        self.start_price = int(start_price.replace(",", ""))
        self.highest_price = int(highest_price.replace(",", ""))
        self.lowest_price = int(lowest_price.replace(",", ""))
        self.trade_volume = int(trade_volume.replace(",", ""))
        self.trade_amount = int(trade_amount.replace(",", ""))
        self.market_cap = int(market_cap.replace(",", ""))
        self.net_cap_value = int(net_cap_value.replace(",", ""))
        self.number_of_share = int(number_of_share.replace(",", ""))
        self.base_index_name = base_index_name
        self.base_index_end_point =  float(base_index_end_point.replace(",", "")) if base_index_end_point != '-' else float("0.00")
        self.base_index_change_point = float(base_index_change_point.replace(",", ""))  if base_index_change_point != '-' else float("0.00")
        self.base_index_change_rate = float(base_index_change_rate.replace(",", "")) if base_index_change_rate != '-' else float("0.00")
    def __str__(self):
        return f"""KrxEtfPrice(date: {self.date}, isu: {self.isu}, name: {self.name}, end_price: {self.end_price}, change_price: {self.change_price}, change_rate: {self.change_rate}, net_value: {self.net_value}, start_price: {self.start_price}, highest_price: {self.highest_price}, lowest_price: {self.lowest_price}, trade_volume: {self.trade_volume}, trade_amount: {self.trade_amount}, market_cap: {self.market_cap}, net_cap_value: {self.net_cap_value}, number_of_share: {self.number_of_share}, base_index_name: {self.base_index_name}, base_index_end_point: {self.base_index_end_point}, base_index_change_point: {self.base_index_change_point}, base_index_change_rate: {self.base_index_change_rate})"""
    def __getitems__(self):
        return [self.date, self.isu, self.name, self.end_price, self.change_price, self.change_rate, self.net_value, self.start_price, self.highest_price, self.lowest_price, self.trade_volume, self.trade_amount, self.market_cap, self.net_cap_value, self.number_of_share, self.base_index_name, self.base_index_end_point, self.base_index_change_point, self.base_index_change_rate]
    def to_dict(self):
        return {'date': self.date.strftime("%Y-%m-%d"), 'isu': self.isu, 'name': self.name, 'end_price': self.end_price, 'change_price': self.change_price, 'change_rate': self.change_rate, 'net_value': self.net_value, 'start_price': self.start_price, 'highest_price': self.highest_price, 'lowest_price': self.lowest_price, 'trade_volume': self.trade_volume, 'trade_amount': self.trade_amount, 'market_cap': self.market_cap, 'net_cap_value': self.net_cap_value, 'number_of_share': self.number_of_share, 'base_index_name': self.base_index_name, 'base_index_end_point': self.base_index_end_point, 'base_index_change_point': self.base_index_change_point, 'base_index_change_rate': self.base_index_change_rate}