import json
import requests
import time
import datetime
import os

from .utils import validate_stock, get_profile, get_financial, get_historical, get_statistic


# params
class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.exchange = ''
        self.sector = ''
        self.status = 0
        self.latest_financial = datetime.date(1970, 1, 1)
        self.latest_historical = datetime.date(1970, 1, 1)
        self.latest_statistic = datetime.date(1970, 1, 1)
        self.data = {
            "financial": None,
            "statistic": None,
            'historical': None
        }

    def retrieve(self):
        try:
            validation = validate_stock(self.symbol)

            if validation['status'] == 'not_exist':
                print('[Error] {} not exists!'.format(self.symbol))
                self.status = -1
                return True
            else:
                if validation['has_profile']:
                    self.sector, self.exchange = get_profile(validation['content'])
                if validation['has_statistics']:
                    self.data['statistic'], self.latest_statistic = get_statistic(self.symbol, self.latest_statistic)
                if validation['has_financial']:
                    self.data['financial'], self.latest_financial = get_financial(self.symbol, self.latest_financial)
                if validation['has_historical']:
                    self.data['historical'], self.latest_historical = get_historical(self.symbol,
                                                                                     self.latest_historical)
                self.status = 0
                return self
        except requests.exceptions.HTTPError as e:
            print('[Error] ' + self.symbol)
            print(str(e))
            self.status = 1
            return False
        except requests.exceptions.ConnectionError as e:
            print('[ConnectionError] ' + self.symbol)
            print(str(e))
            self.status = 1
            return False
        except requests.exceptions.ReadTimeout as e:
            print('[ReadTimeout] ' + self.symbol)
            print(str(e))
            self.status = 1
            return False
        except Exception as e:
            print('[Error] ' + self.symbol)
            print(str(e))
            self.status = 1
            return True

    # Save the result
    def save(self, path='./json'):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            print('Path provided is not a Directory! Check your path!')
            exit(-1)

        filename = '{0} {1}.json'.format(self.symbol, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        with open(os.path.join(path, filename), 'w') as out:
            json.dump({
                'symbol': self.symbol,
                'exchange': self.exchange,
                'sector': self.sector,
                'data': self.data
            }, out)
            print(str(datetime.datetime.now()) + ' Saved {}...'.format(self.symbol))

    def get(self):
        return {
            'symbol': self.symbol,
            'exchange': self.exchange,
            'sector': self.sector,
            'data': self.data
        }
