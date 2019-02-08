from multiprocessing import Process
from .stock import Stock
from .extensions import RF_Stock
import datetime


class StockProcess(Process):
    def __init__(self, symbol, que):
        super(Process, self).__init__()
        self._stock = Stock(symbol=symbol)
        self.que = que

    def run(self):
        print(str(datetime.datetime.now()) + ' Start {}...'.format(self._stock.symbol))
        result = self._stock.retrieve()
        self.que.put(result)
        print(str(datetime.datetime.now()) + ' Finish {}...'.format(self._stock.symbol))


class RF_Process(Process):
    def __init__(self, ticker_obj, que, db_config, server_config):
        super(RF_Process, self).__init__()
        self._stock = RF_Stock(ticker_obj=ticker_obj, db_config=db_config, server_config=server_config)
        self.que = que

    def run(self):
        print(str(datetime.datetime.now()) + ' Start {}...'.format(self._stock.symbol))
        result = self._stock.start()
        if not result:
            self.que.put(self._stock.symbol)
