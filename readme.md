# Korean Stock Market KRX stock data crawler
## Description
- Downloading daily *stock* and *ETF* data crawling from http://data.krx.co.kr/.

- Save data to among or all of
    - PostgreSQL Database
    - ElasticSearch
    - Firestore
    - LocalStorage

## How to use
1. Install requirements
2. If youl'd like to use Postgres, MAKE SURE to create database and tables using `V000*.sql` in root directory
3. Just to crawl or To save

### Just Crawl And Return In List
```python3 
import Crawler
import datetime

once_upon_a_time = Crawler.download_stock(datetime.date(1995, 5, 2))
cap = [stock.market_cap for stock in once_upon_a_time]

print("Korean Stock Market Cap on 1995-May-2 is {}".format(sum(cap)))
 ```


### To Save

#### LocalStorage
```bash
> python3 main.py --local
```

#### Firestore
```bash
> python3 main.py --firestore
```

#### PostgreSQL
```bash
> python3 main.py --postgres
```

#### Elastisearch
```bash
> python3 main.py --elasticsearch
```

#### All
```bash
> python3 main.py --all
```

#### Specify range
```bash
> python3 main.py --all target_date=2021-11-11
```
or range
```bash
> python3 main.py --all from_date=2021-11-01 to_date=2021-11-11
```

### Configuration
`firebase config` is should be located in *project root* as named `firebase_config.json` file
`firebase_config` infomation can be found on [Firebase Doc](https://support.google.com/firebase/answer/7015592?hl=en#zippy=%2Cin-this-article)

The other configuration dat must be written in `config.ini`
In `config.ini` file,
```
[ElasticSearch]
host=localhost

[PostgreSQL]
host=localhost
port=5432
db=finance
user=admin
password=1234

[LocalDownload]
parent_dir=krx
```

`LocalDownload.parent_dir` is the parent folder for downloading location


** This program is ONLY for educational purpose. Repository contiributors are not responsible for any both legal and illegal issues from misuses. **