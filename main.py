from config import *
from extensions import *
import telebot
import requests
import json


coins_list = requests.get(f'https://min-api.cryptocompare.com/data/blockchain/list? or &api_key={API_TOKEN}')
pairs = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'USD': 'USD'
}
for coin in (json.loads(coins_list.content)['Data']):
    pairs.update([(coin, coin)])

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = """Отправьте сообщение боту в виде: <имя валюты цену которой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> \n 
Пример запроса:
BTC USD 10.2

Команда /values покажет доступные валюты"""
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for key in pairs:
        if key != pairs[key]:
            text += f'{key} ({pairs[key]}), '
        else:
            text += f'{key}, '
    bot.reply_to(message, text[:len(text)//2])
    bot.send_message(message.chat.id, text[len(text)//2:-2])


@bot.message_handler(content_types = ['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise InputException()
        quote, base, amount = values
        if quote not in pairs.keys():
            raise CoinNotExist(f'Валюты {quote} нет в базе')
        if base not in pairs.keys():
            raise CoinNotExist(f'Валюты {base} нет в базе')
        if base == quote:
            raise SameCoins()
        try:
            amount = float(amount)
        except:
            raise WrongAmount()

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={pairs[quote]}&tsyms={pairs[base]}')
        total_base = json.loads(r.content)[pairs[base]]

    except APIException as e:
        bot.reply_to(message, e)

    except Exception:
        bot.reply_to(message, 'Упс! Непредвиденная ошибка, попробуйте снова')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base*amount}'
        bot.reply_to(message, text)


bot.polling()

