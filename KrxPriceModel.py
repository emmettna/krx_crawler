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

class KrxEtfPrice:
    # [("isu", "ISU_SRT_CD"), ("name", "ISU_ABBRV"), ("end_price", "TDD_CLSPRC"), ("change_price", "CMPREVDD_PRC"), ("change_rate", "FLUC_RT"), ("net_value", "NAV"), ("start_price", "TDD_OPNPRC"), ("highest_price", "TDD_HGPRC"), ("lowest_price", "TDDLWPRC"), ("trade_volume", "ACC_TRDVOL"), ("trade_amount", "ACC_TRDVAL"), ("market_cap", "MKTCAP"), ("net_cap_value", "INVSTASST_NETASST_TOTAMT"), ("number_of_share", "LIST_SHRS"), ("base_index_name", "IDX_IND_NM"), ("base_index_end_point", "OBJ_STKPRC_IDX"), ("base_index_change_point", "CMPPREVDD_IDX"), ("base_index_change_rate", "FLUC_RT")]
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
        return {'date': self.date, 'isu': self.isu, 'name': self.name, 'end_price': self.end_price, 'change_price': self.change_price, 'change_rate': self.change_rate, 'net_value': self.net_value, 'start_price': self.start_price, 'highest_price': self.highest_price, 'lowest_price': self.lowest_price, 'trade_volume': self.trade_volume, 'trade_amount': self.trade_amount, 'market_cap': self.market_cap, 'net_cap_value': self.net_cap_value, 'number_of_share': self.number_of_share, 'base_index_name': self.base_index_name, 'base_index_end_point': self.base_index_end_point, 'base_index_change_point': self.base_index_change_point, 'base_index_change_rate': self.base_index_change_rate}