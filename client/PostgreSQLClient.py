from model.KrxPriceModel import *
import psycopg2
from psycopg2.extras import execute_values

class PostgreSQL:
    def __init__(self) -> None:
        pass

    def get_connection(host, port, database, user, password):
        return psycopg2.connect(host=host, database=database, user=user, password=password, port=port)

    async def save_stock(rows, conn):    
        cur = conn.cursor()

        for r in rows:
            date = r.date.strftime("%Y-%m-%d")
            cur.execute(
f"""INSERT INTO "korean_stock" (id, date, isu, name, market, sector, end_price, change_price, change_rate, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, number_of_share)
VALUES ('{date +'-'+r.isu}', '{date}', '{r.isu}','{r.name}','{r.market}','{r.sector}',{r.end_price},{r.change_price},{r.change_rate},{r.start_price},{r.highest_price},{r.lowest_price},{r.trade_volume},{r.trade_amount},{r.market_cap},{r.number_of_share})
ON CONFLICT (id) DO NOTHING""")
        conn.commit()

    async def save_eft(rows, conn):    
        cur = conn.cursor()

        for r in rows:
            date = r.date.strftime("%Y-%m-%d")
            cur.execute(
f"""INSERT INTO "korean_etf" (id, date, isu, name, end_price, change_price, change_rate, net_value, start_price, highest_price, lowest_price, trade_volume, trade_amount, market_cap, net_cap_value, number_of_share, base_index_name, base_index_end_point, base_index_change_point, base_index_change_rate)
VALUES ('{date +'-'+r.isu}', '{date}', '{r.isu}', '{r.name}', '{r.end_price}', '{r.change_price}', '{r.change_rate}', '{r.net_value}', '{r.start_price}', '{r.highest_price}', '{r.lowest_price}', '{r.trade_volume}', '{r.trade_amount}', '{r.market_cap}', '{r.net_cap_value}', '{r.number_of_share}', '{r.base_index_name}', '{r.base_index_end_point}', '{r.base_index_change_point}', '{r.base_index_change_rate}')
ON CONFLICT (id) DO NOTHING""")
        conn.commit()

    async def save_stock_base_values(rows, conn) -> None:
        cur = conn.cursor()
        params = [(r.get_unique_id(), r.date, r.isu, r.name, r.end_price, r.eps, r.per, r.forward_eps, r.forward_per, r.bps, r.pbr, r.dps, r.dividend_yield) for r in rows]
        execute_values(cur, """INSERT INTO "korean_stock_base_value" (id, date, isu, name, end_price, eps, per, forward_eps, forward_per, bps, pbr, dps, dividend_yield) VALUES %s ON CONFLICT (id) DO NOTHING""", params)
        cur.close()
        conn.commit()

    async def save_stock_base_value_avg(rows, conn) -> None:
        cur = conn.cursor()
        execute_values(cur, """
        INSERT INTO "korean_stock_base_value" (id, date, name, isu, end_price, eps, per, forward_eps, forward_per, bps, pbr, dps, dividend_yield) 
        VALUES %s ON CONFLICT (id) DO NOTHING""", params)
        cur.close()
        conn.commit()