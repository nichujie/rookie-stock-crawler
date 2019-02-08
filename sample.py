from rookie_stock_crawler import StockCrawler

sc = StockCrawler(['MSFT', 'GOOG', 'AMZN', 'AAPL'])
sc.start()
sc.save_all()

for item in sc:
    print(item.get())
