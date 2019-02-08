import datetime
import calendar
import time
import json
import requests
from bs4 import BeautifulSoup


def get_duration(months):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    total = 0

    for i in range(0, months):
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        total += calendar.monthrange(year, month)[1]

    return total


def parse_date(date_str):
    fmt = '%Y-%m-%d'
    time_tuple = time.strptime(date_str, fmt)
    year, month, day = time_tuple[:3]
    return datetime.date(year, month, day)


def parse_content(content, sec):
    keyw = '"{}"'.format(sec)
    tmp = content.find(keyw)

    if tmp == -1:
        return {}

    while content[tmp + len(keyw) + 1] != '{':
        tmp = content.find(keyw, tmp + 1)
        if tmp == -1:
            return {}

    index = tmp + len(keyw) + 2
    count = 1
    str = '{'

    while count > 0:
        if content[index] == '{':
            count += 1
        if content[index] == '}':
            count -= 1
        str += content[index]
        index += 1

    dic = json.loads(str)
    return dic


def validate_stock(stock):
    result = {}
    url = 'https://finance.yahoo.com/quote/{0}'.format(stock)

    # Test Start
    r = requests.get(url, timeout=45)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    if soup.title is None:
        result['status'] = 'not_exist'
        return result

    title = soup.title.get_text()
    if not title.startswith(stock):
        result['status'] = 'not_exist'
        return result

    has_financial = False
    has_statistics = False
    has_profile = False
    has_historical = False
    lis = soup.find(class_='fin-tab-items')

    for li in lis:
        if li.get_text() == 'Financials':
            has_financial = True
        if li.get_text() == 'Statistics':
            has_statistics = True
        if li.get_text() == 'Profile':
            has_profile = True
        if li.get_text() == 'Historical Data':
            has_historical = True
    # Test End

    result['status'] = 'normal'
    result['content'] = r.text
    result['has_financial'] = has_financial
    result['has_statistics'] = has_statistics
    result['has_profile'] = has_profile
    result['has_historical'] = has_historical
    return result


def get_profile(content):
    profile = parse_content(content, 'summaryProfile')
    type = parse_content(content, 'quoteType')
    sector = profile.get('sector', '')
    exchange = type.get('exchange', '')
    return sector, exchange


def get_financial(symbol, lf=datetime.date(1970, 1, 1)):
    latest_financial = lf
    result = {}
    url = 'https://finance.yahoo.com/quote/{0}/financials?p={0}'.format(symbol)
    annual = ['incomeStatementHistory', 'balanceSheetHistory', 'cashflowStatementHistory']
    # quarter = ['incomeStatementHistoryQuarterly', 'balanceSheetHistoryQuarterly', 'cashflowStatementHistoryQuarterly']

    r = requests.get(url, timeout=45)
    r.raise_for_status()

    tmp = parse_content(r.text, annual[0]).get('incomeStatementHistory', [])
    for item in tmp:
        if result.get(item['endDate']['fmt'], None) is None:
            result[item['endDate']['fmt']] = {
                'IS': {},
                'BS': {},
                'CF': {}
            }
        result[item['endDate']['fmt']]['IS'] = item

    tmp = parse_content(r.text, annual[1]).get('balanceSheetStatements', [])
    for item in tmp:
        if result.get(item['endDate']['fmt'], None) is None:
            result[item['endDate']['fmt']] = {
                'IS': {},
                'BS': {},
                'CF': {}
            }
        result[item['endDate']['fmt']]['BS'] = item

    tmp = parse_content(r.text, annual[2]).get('cashflowStatements', [])
    for item in tmp:
        if result.get(item['endDate']['fmt'], None) is None:
            result[item['endDate']['fmt']] = {
                'IS': {},
                'BS': {},
                'CF': {}
            }
        result[item['endDate']['fmt']]['CF'] = item

    data = []
    for key, value in result.items():
        date = parse_date(key)
        if date > lf:
            latest_financial = max(date, latest_financial)
            data.append({'date': key, 'financial': value})

    if len(data) == 0:
        data = None
    return data, latest_financial


def get_statistic(symbol, ls=datetime.date(1970, 1, 1)):
    latest_statistic = ls
    url = 'https://finance.yahoo.com/quote/{0}/key-statistics?p={0}'.format(symbol)
    statistics = 'defaultKeyStatistics'
    r = requests.get(url, timeout=45)
    r.raise_for_status()
    result = parse_content(r.text, statistics)
    if result == {}:
        return None, ls
    if datetime.datetime.utcnow().date() > latest_statistic:
        return result, datetime.datetime.utcnow().date()
    else:
        return None, datetime.datetime.utcnow().date()


def get_historical(stock, lh=datetime.date(1970, 1, 1), duration=9):
    latest_historical = lh
    period2 = int(time.time())
    period1 = period2 - 86400 * get_duration(duration)

    url = 'https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d'.format(
        stock, period1, period2)

    r = requests.get(url, timeout=45)
    r.raise_for_status()
    prices = parse_content(r.text, 'HistoricalPriceStore').get('prices', [])
    result = []

    # delete dividend data
    for i in range(len(prices) - 1, -1, -1):
        if 'type' in prices[i].keys():
            prices.pop(i)
        else:
            date = datetime.date.fromtimestamp(prices[i]['date'])
            if date > lh:
                latest_historical = max(date, latest_historical)
                result.append(prices[i])

    if len(result) == 0:
        result = None
    return result, latest_historical
