# Korean Stock Market KRX stock data crawler
## Description
- Downloading daily *stock* and *ETF* data crawling from http://data.krx.co.kr/.

- Save data to among or all of
    - PostgreSQL Database
    - ElasticSearch
    - Firestore
    - LocalStorage

## How to use
- Either download as list or save

### Just Crawl And Return In List
```python3 
import Crawler
import datetime

once_upon_a_time = Crawler.download_stock(datetime.date(1995, 5, 2))
cap = [stock.market_cap for stock in once_upon_a_time]

print("Korean Stock Market Cap on 1995-May-2 is {}".format(sum(cap)))
 ```


### Save


#### LocalStorage

#### Firestore

#### PostgreSQL

#### Elastisearch


** This program is ONLY for educational purpose. Repository contiributors are not responsible for any both legal and illegal issues from misuses. **