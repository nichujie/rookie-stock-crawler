# py-stock-crawler
A multithreading web crawler that retrieves stock data from yahoo finance.



## Usage 

Extremely easy to use!

Use three lines to create a multi-thread crawler and save the data to local as json files.

```python
from rookie_stock_crawler import StockCrawler

sc = StockCrawler(['MSFT', 'GOOG', 'AMZN', 'AAPL'])
sc.start()
sc.save_all()
```

