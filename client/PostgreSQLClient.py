from model.KrxPriceModel import *
import psycopg2
from dateutil.relativedelta import relativedelta
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

    async def save_stock_base_value_avg(conn, today) -> None:
        cur = conn.cursor()
        today_str = today.strftime("%Y-%m-%d")
        ten_years_ago_str = (today - relativedelta(years=10)).strftime("%Y-%m-%d")
        cur.execute(f"""
        INSERT INTO "korean_stock_base_value_average" (id, date, name, isu, per, pbr, bps, dividend_yield, eps, dps) 
            WITH avg_table AS(
                SELECT '{today_str}'::DATE, isu, AVG(per) AS per, AVG(pbr) AS pbr, AVG(bps) as bps, AVG(dividend_yield) AS dividend_yield, AVG(eps) AS eps, AVG(dps) as dps FROM korean_stock_base_value 
                WHERE date > '{ten_years_ago_str}' AND date <= '{today_str}' GROUP BY isu)
            SELECT date || '-' || isu AS id, date, (select name from korean_stock_base_value where isu = avg_table.isu limit 1), isu, per, pbr, bps, dividend_yield, eps, dps FROM avg_table
        ON CONFLICT (id) DO NOTHING""")
        cur.close()
        conn.commit()

    async def upsert_under_valued_assets_to_cache(conn, target_date) -> None:
        # id, date, isu, name, end_price, current_per, current_pbr, current_dividend_yield, average_per, average_pbr, average_dividend_yield, average_values_price, discount_rate
        cur = conn.cursor()
        target_date_str = target_date.strftime("%Y-%m-%d")
        cur.execute(f"""
        INSERT INTO "korean_stock_undervalued_cache" (id, date, isu, name, end_price, current_per, current_pbr, current_dividend_yield, average_per, average_pbr, average_dividend_yield, average_values_price, discount_rate) 
            WITH korean_stock_value_merged AS(
                SELECT t1.isu, t2.name, t2.date, t2.end_price, t1.per AS avg_per, t2.per AS cur_per,
                    CASE WHEN t2.per != 0 then t1.per * t2.eps else NULL end AS avg_per_price,
                    t1.pbr as avg_pbr, t2.pbr as cur_pbr,
                    CASE WHEN t2.pbr != 0 then t1.pbr * t2.bps else NULL end AS avg_pbr_price,
                    t1.dividend_yield as avg_dividendYield, t2.dividend_yield AS cur_dividend_yield,
                    CASE WHEN t2.dividend_yield != 0 then t2.dps * 100 / t1.dividend_yield else NULL END AS avg_dividend_yield_price
                    FROM korean_stock_base_value_average AS t1
                    LEFT JOIN korean_stock_base_value AS t2 ON t1.id = t2.id
                LEFT JOIN korean_stock AS t3 on t1.id = t3.id
                WHERE t3.market_cap > 100000000000 AND t3.end_price >= 1000 AND t3.date <= '{target_date_str}'),
            result_table AS(SELECT date, isu, name, end_price,
                cur_per,
                cur_pbr,
                cur_dividend_yield,
                avg_per_price,
                avg_pbr_price,
                avg_dividend_yield_price,
                (select avg(a1) avg_price from (values (avg_dividend_yield_price), (avg_per_price), (avg_pbr_price)) as anonymous (a1) where a1 != 0)::NUMERIC(10, 2) as average_values_price,
                ((select avg(a1) avg_price from (values (avg_dividend_yield_price), (avg_per_price), (avg_pbr_price)) as anonymous (a1) where a1 != 0)::NUMERIC(10, 2) - end_price) / end_price as discount_rate
                FROM korean_stock_value_merged ORDER BY discount_rate DESC)
            SELECT date || '-' || isu as id, date, isu, name, end_price, cur_per, cur_pbr, cur_dividend_yield, avg_per_price, avg_pbr_price, avg_dividend_yield_price, average_values_price, discount_rate
            FROM result_table WHERE discount_rate IS NOT NULL AND date = '{target_date_str}'
        ON CONFLICT (id) DO UPDATE SET 
            name = EXCLUDED.name,
            end_price = EXCLUDED.end_price,
            cur_per = EXCLUDED.cur_per, 
            cur_pbr = EXCLUDED.cur_pbr, 
            cur_dividend_yield = EXCLUDED.cur_dividend_yield, 
            avg_per_price = EXCLUDED.avg_per_price, 
            avg_pbr_price = EXCLUDED.avg_pbr_price, 
            avg_dividend_yield_price = EXCLUDED.avg_dividend_yield_price, 
            average_values_price = EXCLUDED.average_values_price, 
            discount_rate = EXCLUDED.discount_rate""")
        cur.close()
        conn.commit()