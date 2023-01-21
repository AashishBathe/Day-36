import os
import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API = os.environ.get("STOCK_API")
NEWS_API = os.environ.get("NEWS_API")
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

parameters = {
    "symbol": STOCK,
    "apikey": API,
    "function": "TIME_SERIES_DAILY_ADJUSTED"
}

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
today = dt.date.today()
yesterday = str(today - dt.timedelta(days=1))
day_before_yesterday = str(today - dt.timedelta(days=2))
response = requests.get('https://www.alphavantage.co/query', params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
yesterday_close = float(data[yesterday]["4. close"])
day_before_yesterday_close = float(data[day_before_yesterday]["4. close"])
percent = ((yesterday_close - day_before_yesterday_close) / day_before_yesterday_close * 100)
if abs(percent) <= 5:
    if percent < 0:
        symbol = '🔻'
    else:
        symbol = '🔺'

    news_param = {
        "q": "tesla",
        "from": yesterday,
        "apiKey": NEWS_API
    }
    news = requests.get("https://newsapi.org/v2/everything", params=news_param)
    news.raise_for_status()
    news_data = news.json()["articles"]
    data1_title = news_data[0]["title"]
    data1_description = news_data[0]["description"]
    data2_title = news_data[1]["title"]
    data2_description = news_data[1]["description"]
    data3_title = news_data[2]["title"]
    data3_description = news_data[2]["description"]
    news_final = f"\n{STOCK}: {symbol}{round(abs(percent), 2)}%\nHeadline: {data1_title} \nBrief: {data1_description} \nHeadline: {data2_title} \nBrief: {data2_description} \nHeadline: {data3_title} \nBrief: {data3_description}"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=news_final,
        from_="TRIAL_NUMBER",
        to="YOUR_NUMBER"
    )
    print(message.status)

