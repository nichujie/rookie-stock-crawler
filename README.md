# py-stock-crawler
A multithreading web crawler that retrieves stock data from yahoo finance.



## Usage 

Extremely easy to install, no extra C or binary libs required! 

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

## Exceptions

This package do not offer any customized exceptions. However, all exceptions raised during crawling are caught and printed with a prefix tag like **"[Error]"**. This is designed not to interrupt the crawling, in which case all the data will lose if you do not set the **auto_save** option to **True**.

All the exceptions raised outside crawling will still interrupt the program.