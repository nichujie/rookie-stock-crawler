import psycopg2
import psycopg2.extras
from datetime import datetime

psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)


# In multi-thread programming(crawlers), every thread shall have its
# own connection with database, or else it will raise a SSL exception.
class RF_Database:
    def __init__(self, symbol, config):
        if config == None:
            print('No configuration for databse is provided!')
            exit(-1)

        self._conn = psycopg2.connect(host=config['HOST'],
                                      dbname=config['DB_NAME'],
                                      user=config['USER'],
                                      password=config['PASSWD'])
        self._cur = self._conn.cursor()
        self._symbol = symbol

    # Iterate the content in the cursor
    def __iter__(self):
        return self._cur

    # In case there is unexpected exit
    def __del__(self):
        self._conn.commit()
        self._cur.close()
        self._conn.close()

    def execute(self, statement, values):
        self._cur.execute(statement, values)

    def commit(self):
        self._conn.commit()

    def update_financial(self, data):
        self._cur.execute('SELECT * FROM public.stock_financial WHERE name=%s;', (self._symbol,))
        if self._cur.rowcount > 0:
            self._cur.execute(
                '''UPDATE public.stock_financial SET data = data || %s::jsonb[], update_time = %s WHERE name=%s''',
                (data, datetime.now(), self._symbol,))
        else:
            self._cur.execute(
                "INSERT INTO public.stock_financial (name, data, update_time) VALUES (%s, %s::jsonb[], %s)",
                (self._symbol, data, datetime.now()))

    def update_statistic(self, data):
        self._cur.execute('SELECT * FROM public.stock_statistic WHERE name=%s;', (self._symbol,))
        if self._cur.rowcount > 0:
            self._cur.execute(
                '''UPDATE public.stock_statistic SET data = %s, update_time = %s WHERE name=%s''',
                (data, datetime.now(), self._symbol,))
        else:
            self._cur.execute(
                "INSERT INTO public.stock_statistic (name, data, update_time) VALUES (%s, %s, %s)",
                (self._symbol, data, datetime.now()))

    def update_historical(self, data):
        self._cur.execute('SELECT * FROM public.stock_historical WHERE name=%s;', (self._symbol,))
        if self._cur.rowcount > 0:
            self._cur.execute(
                '''UPDATE public.stock_historical SET data = data || %s::jsonb[], update_time = %s WHERE name=%s''',
                (data, datetime.now(), self._symbol,))
        else:
            self._cur.execute(
                "INSERT INTO public.stock_historical (name, data, update_time) VALUES (%s, %s::jsonb[], %s)",
                (self._symbol, data, datetime.now()))

    def upload(self, data):
        if data.get('financial', None) is not None:
            self.update_financial(data['financial'])
        if data.get('statistic', None) is not None:
            self.update_statistic(data['statistic'])
        if data.get('historical', None) is not None:
            self.update_historical(data['historical'])
        self._conn.commit()
