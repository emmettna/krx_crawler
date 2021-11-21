import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="finance",
    user="admin",
    password="1234")

select_all_company_isu = """SELECT isu FROM korean_stock group by isu"""

def stock_bulk(isu: str):
    return """insert into korean_stock_moving_average
select (date || '-' || isu) as id, date, name,
avg(start_price) over (order by "date" asc rows between 3 preceding and current row)::BIGINT as start_price_3,
avg(start_price) over (order by "date" asc rows between 5 preceding and current row)::BIGINT as start_price_5,
avg(start_price) over (order by "date" asc rows between 7 preceding and current row)::BIGINT as start_price_7,
avg(start_price) over (order by "date" asc rows between 10 preceding and current row)::BIGINT as start_price_10,
avg(start_price) over (order by "date" asc rows between 15 preceding and current row)::BIGINT as start_price_15,
avg(start_price) over (order by "date" asc rows between 25 preceding and current row)::BIGINT as start_price_25,
avg(start_price) over (order by "date" asc rows between 50 preceding and current row)::BIGINT as start_price_50,
avg(start_price) over (order by "date" asc rows between 100 preceding and current row)::BIGINT as start_price_100,
avg(start_price) over (order by "date" asc rows between 120 preceding and current row)::BIGINT as start_price_120,
avg(end_price) over (order by "date" asc rows between 3 preceding and current row)::BIGINT as end_price_3,
avg(end_price) over (order by "date" asc rows between 5 preceding and current row)::BIGINT as end_price_5,
avg(end_price) over (order by "date" asc rows between 7 preceding and current row)::BIGINT as end_price_7,
avg(end_price) over (order by "date" asc rows between 10 preceding and current row)::BIGINT as end_price_10,
avg(end_price) over (order by "date" asc rows between 15 preceding and current row)::BIGINT as end_price_15,
avg(end_price) over (order by "date" asc rows between 25 preceding and current row)::BIGINT as end_price_25,
avg(end_price) over (order by "date" asc rows between 50 preceding and current row)::BIGINT as end_price_50,
avg(end_price) over (order by "date" asc rows between 100 preceding and current row)::BIGINT as end_price_100,
avg(end_price) over (order by "date" asc rows between 120 preceding and current row)::BIGINT as end_price_120,
avg(highest_price) over (order by "date" asc rows between 3 preceding and current row)::BIGINT as highest_price_3,
avg(highest_price) over (order by "date" asc rows between 5 preceding and current row)::BIGINT as highest_price_5,
avg(highest_price) over (order by "date" asc rows between 7 preceding and current row)::BIGINT as highest_price_7,
avg(highest_price) over (order by "date" asc rows between 10 preceding and current row)::BIGINT as highest_price_10,
avg(highest_price) over (order by "date" asc rows between 15 preceding and current row)::BIGINT as highest_price_15,
avg(highest_price) over (order by "date" asc rows between 25 preceding and current row)::BIGINT as highest_price_25,
avg(highest_price) over (order by "date" asc rows between 50 preceding and current row)::BIGINT as highest_price_50,
avg(highest_price) over (order by "date" asc rows between 100 preceding and current row)::BIGINT as highest_price_100,
avg(highest_price) over (order by "date" asc rows between 120 preceding and current row)::BIGINT as highest_price_120,
avg(lowest_price) over (order by "date" asc rows between 3 preceding and current row)::BIGINT as lowest_price_3,
avg(lowest_price) over (order by "date" asc rows between 5 preceding and current row)::BIGINT as lowest_price_5,
avg(lowest_price) over (order by "date" asc rows between 7 preceding and current row)::BIGINT as lowest_price_7,
avg(lowest_price) over (order by "date" asc rows between 10 preceding and current row)::BIGINT as lowest_price_10,
avg(lowest_price) over (order by "date" asc rows between 15 preceding and current row)::BIGINT as lowest_price_15,
avg(lowest_price) over (order by "date" asc rows between 25 preceding and current row)::BIGINT as lowest_price_25,
avg(lowest_price) over (order by "date" asc rows between 50 preceding and current row)::BIGINT as lowest_price_50,
avg(lowest_price) over (order by "date" asc rows between 100 preceding and current row)::BIGINT as lowest_price_100,
avg(lowest_price) over (order by "date" asc rows between 120 preceding and current row)::BIGINT as lowest_price_120
from korean_stock where isu = '{}' order by "date" desc
ON CONFLICT (id) DO NOTHING""".format(isu)

cur = conn.cursor()
cur.execute(select_all_company_isu)

isus = [a[0] for a in cur.fetchall()]

for isu in isus:
    print(isu)
    cur.execute(stock_bulk(isu))
conn.commit()

conn.close()