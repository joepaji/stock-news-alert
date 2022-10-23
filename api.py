from urllib import parse
import requests

STOCK_API_URL = 'https://www.alphavantage.co/query'
NEWS_API_URL = 'https://newsapi.org/v2/everything'
STOCK_API_KEY = 'AL5KGRE0FRBIFZ0P'
NEWS_API_KEY = 'e5aa7b0673c74f42a2e464f45980256a'

def get_stock_data(symbol):
    parameters = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol.upper(),
        'apikey': STOCK_API_KEY
    }
    response = requests.get(STOCK_API_URL, params=parameters)
    if response is not None and response.ok:
        data = response.json()
    else:
        response.raise_for_status()

    return data

def get_article_data(company):
    company = parse.quote_plus(company)
    parameters = {
        'q': company,
        'sortBy': "relevancy",
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=parameters)
    if response is not None and response.ok:
        data = response.json()
    else:
        response.raise_for_status()

    return data