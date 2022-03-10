import responses as r
import yfinance as yf
import os
import telebot
from telegram.ext import *
from pycoingecko import CoinGeckoAPI
import environs
from datetime import datetime


API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot("5081651763:AAEuxQKeMN8zBmYCwP1FAIkw5-kLmZ66HUI")

print("Bot booting up...")

# messages input

greetings_list = ["hello","hi", "sup","hey","hiya"]
@bot.message_handler(func=lambda message: message.text.lower() in greetings_list)
def reply(message):
    text = str(message.text).lower()
    responses = r.sample_responses(text)
    bot.reply_to(message)


# responses
@bot.message_handler(commands=['start'])
def help(message):
    bot.reply_to(message, "Welcome to Arthur's Crypto Bot!")

@bot.message_handler(commands=['who'])
def help(message):
    bot.reply_to(message, "I was created by Arthur! An aspiring computer scientist from Singapore! Stay tuned for more projects like this!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "A list of commands you can try are\n/portfolio - see some stocks I like\n/who - about me\nor simply try 'price (stock/CryptoName)' and I will find it for you!")


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "hello there!")


# stocks 

@bot.message_handler(commands=['portfolio'])
def get_stocks(message):
    response = ""
    stocks = ['TSLA','AAPL','TCEHY','AMZN','GOOGL',"^"'GSPC']
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period= '2d', interval= '1d')
        data = data.reset_index()
        response += f"-----{stock}-----\n"
        stock_data.append([stock])
        columns = ['Stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) -1
            price= round(row['Close'],2)
            format_date= row['Date'].strftime('%d/%m')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()
    
    response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
    response += "\nStock Data for today"
    print(response)
    bot.send_message(message.chat.id,response)
    

def stock_request(message):
    request = message.text.split()
    if len(request) <2 or request[0].lower() not in " price":
        return False
    else:
        return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request= message.text.split()[1]
    data = yf.download(tickers= request, period= '60m', interval= '15m')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"]= data['Datetime'].dt.strftime('%d/%m %I:%M %p')
        data.set_index('format_date',inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id,data['Close'].to_string(header=False))
    else:
        bot.send_message(message.chat.id,"No data received")




# crypto 

coin_client= CoinGeckoAPI()



@bot.message_handler(commands=['crypto'])
def crypto(message):
    crypto.id= message.text.lower()
    price_response= coin_client.get_price(ids=crypto.id, vs_currencies= 'usd')

    if price_response:
        price= price_response[crypto.id]['usd']
        bot.send_message(chat_id=message.chat.id, text=f"Price of {crypto.id}: {price}")
    else:
        bot.send_message(chat_id=message.chat.id, text=f"Crypto {crypto.id} was not found")




bot.polling()
