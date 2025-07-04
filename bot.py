import asyncio
from telebot.async_telebot import AsyncTeleBot, types
from proverka import *
from sql import *
from test_create import *
import requests

PATH = 'C:\\Users\\basda\\OneDrive\\Рабочий стол\\token.txt'
TOKEN = open(PATH).readline()
requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1').json()

bot = AsyncTeleBot(TOKEN)

async def send(id, text):
    await bot.send_message(id, text)

creators = set()

@bot.message_handler(commands=['start'])
async def welcome(message):
    start(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Создать тест', 'Мои тесты', 'Друзья', row_width=1)
    await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if (message.text == 'Создать тест' and message.from_user.id not in creators):
        creators.add(message.from_user.id)
        await bot.send_message(message.chat.id, 'Давайте начнем!\n\nВведите название теста:')
    elif (message.from_user.id in creators):
        create_test(message)
    else:
        await bot.send_message(message.chat.id, 'Не понял вас')

asyncio.run(bot.polling())