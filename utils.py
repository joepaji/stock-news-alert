from datetime import date
from datetime import timedelta
from api import get_stock_data, get_article_data
from twilio.rest import Client
import os
import html
import re

def get_last_two_days(offset=0):
    """Gets the date of the last two days"""
    today = date.today()
    start_date = today - timedelta(days=offset)
    day1 = start_date - timedelta(days=1)
    day2 = day1 - timedelta(days=1)

    return str(day1), str(day2)

def get_close_diff(stock):
    """Gets the closing price difference between last 2 days."""
    DAILY_KEY = "Time Series (Daily)"
    CLOSE_KEY = "4. close"
    data = get_stock_data(stock)[DAILY_KEY]
    today = str(date.today())
    day1, day2 = get_last_two_days()
    if today in data:
        close1 = float(data[today][CLOSE_KEY])
    else:
        offset = 0
        while not day1 in data:
            offset += 1
            day1, day2 = get_last_two_days(offset)
        close1 = float(data[day1][CLOSE_KEY])
    close2 = float(data[day2][CLOSE_KEY])
    diff = close1 - close2
    percent_change = (diff/close2)*100
    
    return round(percent_change, 2)

def get_top_articles(company):
    """Gets top 3 articles for given company name."""
    data = get_article_data(company)['articles']
    articles = []
    for i in range(0,3):
        article_data = data[i]
        title = html.unescape(article_data['title'])
        title = clean_html(title)
        description = html.unescape(article_data['description'])
        description = clean_html(description)
        article = {
            "title": title,
            "description": description,
            "url": article_data['url']
        }
        articles.append(article)

    return articles

def send_message(message):
    """Sends message"""
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+18582408124',
        to='+14802739636',
        body=message
    )

def build_message_body(symbol, company_name):
    """Builds SMS body based on stock symbol and given articles"""
    articles = get_top_articles(company_name)
    body = f"{symbol}: "
    close_diff = get_close_diff(symbol)
    if close_diff<0:
        body += f'🔻{close_diff}%\n'
    else:
        body += f'🔺{close_diff}%\n'
    for article in articles:
        body += f"Headline: {article['title']}\n"
        body += f"Brief: {article['description']}\n"
        body += f"URL: {article['url']}\n\n"
    
    return body

def clean_html(raw_html):
    """Removes all html tags from string"""
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext