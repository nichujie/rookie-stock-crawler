import datetime
import requests
import json

from .stock import Stock
from .database import RF_Database
from .utils import parse_date

class RF_Stock(Stock):
    def __init__(self, ticker_obj, db_config, server_config):
        super().__init__(ticker_obj['name'])
        self.exchange = ticker_obj['exchange']
        self.sector = ticker_obj['sector']
        self.latest_financial = datetime.date(1970, 1, 1) if (ticker_obj['latest_financial'] is None) else parse_date(ticker_obj[
            'latest_financial'])
        self.latest_historical = datetime.date(1970, 1, 1) if (ticker_obj['latest_historical'] is None) else parse_date(ticker_obj[
            'latest_historical'])
        self.latest_statistic = datetime.date(1970, 1, 1) if (ticker_obj['latest_statistic'] is None) else parse_date(ticker_obj[
            'latest_statistic'])
        self.db = RF_Database(symbol=self.symbol, config=db_config)
        self.server = server_config

    def update(self):
        data = {
            'name': self.symbol,
            'sector': self.sector,
            'exchange': self.exchange,
            'status': self.status,
            'latest_financial': str(self.latest_financial),
            'latest_statistic': str(self.latest_statistic),
            'latest_historical': str(self.latest_historical)
        }
        headers = {'Content-Type': 'application/json'}
        requests.put(url=self.server['host'] + 'crawler/ticker',
                     headers=headers,
                     data=json.dumps(data),
                     timeout=20)

    def start(self):
        result = self.retrieve()
        self.db.upload(self.data)
        self.update()
        return result
