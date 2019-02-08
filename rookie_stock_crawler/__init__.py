name = 'rookie-stock-crawler'
__all__ = ['StockCrawler', 'RF_Crawler']

import json
import requests
import datetime
import time
from multiprocessing import Manager

from .process import StockProcess, RF_Process
from .stock import Stock


class StockCrawler:
    def __init__(self, symbol_list, concurrent=5, auto_save=False, auto_sleep=None):
        self.concur = concurrent
        self.symbol_list = symbol_list
        self.data = []
        self.auto_save = auto_save
        if auto_sleep == True:
            self.auto_sleep = 10 * 60
        else:
            self.auto_sleep = auto_sleep

    def __iter__(self):
        return iter(self.data)

    def start(self):
        # Save all processes
        process_list = []
        que = Manager().Queue()
        count = 0

        # Create and start processes
        for symbol in self.symbol_list:
            count += 1
            p = StockProcess(symbol=symbol, que=que)
            p.daemon = True
            p.start()
            process_list.append(p)
            if count == self.concur or symbol == self.symbol_list[-1]:
                count = 0

                # Wait for the sub processes
                for i in process_list:
                    i.join(timeout=45)

                will_sleep = False
                while not que.empty():
                    res = que.get()
                    if (not res) and self.auto_sleep:
                        will_sleep = True
                    elif type(res) == Stock:
                        self.data.append(res)
                        if self.auto_save:
                            res.save()
                if will_sleep:
                    print(str(datetime.datetime.now()) + ' Start Sleeping...')
                    print('Restart after {} seconds...'.format(self.auto_sleep))
                    time.sleep(self.auto_sleep)
                    print('===' * 20)
                    print(str(datetime.datetime.now()) + ' Finish Sleeping...')

    def save_all(self):
        for item in self.data:
            item.save()


class RF_Crawler:
    def __init__(self, db_config, server_config, concurrent=5):
        if (db_config is None) or (server_config is None):
            print('RF_Crawler: Wrong params!')
            exit(-1)
        self.db_config = db_config
        self.server_config = server_config
        self._concur = concurrent

    def get_tickers(self, count):
        data = {'count': count}
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url=self.server_config['host'] + 'crawler/ticker', headers=headers,
                                data=json.dumps(data))
        tmp = json.loads(response.text)
        return tmp

    def start(self):
        symbol_list = self.get_tickers(self._concur)
        # Save all processes
        process_list = []
        que = Manager().Queue()

        # Create and start processes
        for ticker in symbol_list:
            p = RF_Process(ticker, que, self.db_config, self.server_config)
            p.daemon = True
            p.start()
            process_list.append(p)

        # Wait for the sub processes
        for i in process_list:
            i.join(timeout=45)

        if not que.empty():
            while not que.empty():
                que.get()
            print(datetime.datetime.now())
            print('404 sleeping...')
            time.sleep(10 * 60)
