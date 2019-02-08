from rookie_stock_crawler import StockCrawler

sc = StockCrawler(['MSFT', 'GOOG', 'AMZN', 'AAPL'])
sc.start()
sc.save_all()

for item in sc:
    print(item.get())

##################################################

from rookie_stock_crawler.stock import Stock

st = Stock('AAPL')
st.retrieve()
st.save()
print(st.get())

##################################################

from rookie_stock_crawler.utils import get_financial, get_statistic, get_historical

symbol = 'AAPL'
print(get_financial(symbol))
print(get_statistic(symbol))
print(get_historical(symbol))
