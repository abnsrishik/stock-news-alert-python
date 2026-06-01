import os
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API = os.environ.get("STOCK_API")

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = os.environ.get("NEWS_API")

to_whatsapp_num = os.environ.get("TO_WHATSAPP_NUMBER")

stock_params = {
    'function' : 'TIME_SERIES_DAILY',
    'symbol' : STOCK_NAME,
    'apikey' : STOCK_API,
}


stock_response = requests.get(url = STOCK_ENDPOINT, params= stock_params) #request STOCK API
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)'] # get data from stock api in json format

stock_data_list = [values for keys, values in stock_data.items()]
yesterday_stock = float(stock_data_list[0]['4. close'])
day_before_yesterday_stock = float(stock_data_list[1]['4. close'])

diff = yesterday_stock - day_before_yesterday_stock # comparing yesterday and day before yesterday stock

up_down = None

if diff > 0:
    up_down = "🔺" # just to add string
else:
    up_down = "🔻"

diff_percent = round((diff/yesterday_stock) * 100) # on what percentage they vary

if abs(diff_percent) > 5: # comparing to 5%, just to get new if difference is more than 5%
    news_params = {
        'apikey': NEWS_API,
        'qInTitle': COMPANY_NAME, # Get only given company related news
        'sortBy': 'popularity'
    }
    news_response = requests.get(url = NEWS_ENDPOINT, params=news_params) # request to access data from NEWS API
    articles = news_response.json()['articles'][:3] # first 3 articles

    formatted_articles = [(f"{STOCK_NAME} {up_down}{diff_percent}%\nHeadline: {article['title']}."
                          f"\nBrief: {article['description']}.")for article in articles] # formating the text message

    client = Client(account_sid, auth_token)
    for article in formatted_articles: # get three different messages

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body = article,
            to = to_whatsapp_num
        )
        print(message.status)