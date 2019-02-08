# py-stock-crawler
A multithreading web crawler that retrieves stock data from yahoo finance.

## Usage 

Extremely easy to install !!! No extra C or binary libs required !!!

Only python 3 supported.

```bash
pip install rookie-stock-crawler
```

Use four lines to create a multi-thread crawler and save the data to local as json files.

```python
from rookie_stock_crawler import StockCrawler

sc = StockCrawler(['MSFT', 'GOOG', 'AMZN', 'AAPL'])
sc.start()
sc.save_all()
```

The crawler object is iterable:

```python
for item in sc:
    print(item.get())
```



## Settings

#### class StockCrawler(symbol_list, concurrent=5, auto_save=False, auto_sleep=None)[[Source]](https://github.com/nichujie/rookie-stock-crawler/blob/master/rookie_stock_crawler/__init__.py#L15)

##### symbol_list

A list containing the symbols you want to crawl. The symbol must exist at yahoo finance or it will print some message to notify you(will not raise an exception).

##### concurrent

An integer. The number of processes the program will start at one time to crawl data. Each process retrieves one stock.

##### auto_save

**True** or **False**. If set to **True**, the data of a stock will save instantly after crawled. 

##### auto_sleep

**None**, **True**, or any positive integer. This param decides how many seconds the crawler will sleep after yahoo start to return 404 response (which means your client has reached its accessing limits).

If set to true, it will sleep 600 seconds by default.

## Utilities

The whole package is designed to be detachable. All methods and object can be imported and used independently.

#### class Stock[[Source]](https://github.com/nichujie/rookie-stock-crawler/blob/master/rookie_stock_crawler/stock.py#L11)

The main object stored in the crawler. The variable **item** in the code above is a Stock object. Which means you can access its attributes directly or use other methods.

```python
from rookie_stock_crawler.stock import Stock

st = Stock('AAPL')
st.retrieve()
st.save()
print(st.get())
```

This is an example of creating a single small crawler without multi-thread.

#### rookie_stock_crawler.utils[[Source]](https://github.com/nichujie/rookie-stock-crawler/blob/master/rookie_stock_crawler/utils.py)

As we keep on breaking down the modules, we can import the methods whick **Stock** used to retrieve data. They works almost like a pure function(as long as your home router didn't explode).

```python
from rookie_stock_crawler.utils import get_financial, get_statistic, get_historical

symbol = 'AAPL'
print(get_financial(symbol))
print(get_statistic(symbol))
print(get_historical(symbol))
```

All methods return a tuple of length 2. The first element is stock data(a list or dict), and the second one is the latest date of the data (e.g. The latest financial of Apple Inc. was released on 2018-9-29).

## Exceptions

This package do not offer any customized exceptions. However, all exceptions raised during crawling are caught and printed with a prefix tag like **"[Error]"**. This is designed not to interrupt the crawling, in which case all the data will lose if you do not set the **auto_save** option to **True**.

All the exceptions raised outside crawling will still interrupt the program.

## Special Instructions

Yahoo finance no longer maintain its API or YQL query. As a result, we cannot know the exact limit of accesing frequency. The crawler actually get the data by directly sending request to the server, which is exactly the same as you open a browser and visit the yahoo website.

In other words, you cannot crawl huge amount of data in a short time. It's already enough for individual developers and crawler fans. But if you want to get faster, the package also provide a distributed version to run on different servers. The whole solution includes a Django server and a front end. 

If you are interested, you can visit my other repos, or else you can try other methods like fake-useragent (🤣that won't work) or global proxies(🤪may also not work), etc.