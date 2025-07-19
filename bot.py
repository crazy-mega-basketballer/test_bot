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
testers = set()

@bot.message_handler(commands=['start'])
async def welcome(message):
    start(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест друга', row_width=1)
    await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
async def echo_message(message):

    if (message.text == 'Создать тест' and message.from_user.id not in creators):
        creators.add(message.from_user.id)
        await bot.send_message(message.chat.id, 'Давайте начнем!\n\nВведите название теста:')

    elif (message.from_user.id in creators):
        if create_test(message):
            creators.remove(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест друга', row_width=1)
            await bot.send_message(message.chat.id, 'Готово!', reply_markup=markup)
    
    elif (message.text == 'Мои тесты' and message.from_user.id not in creators):
        tests = select('tests', colums = 'test_id, name', where = f'user_id = "{message.from_user.id}"')
        if (len(tests) > 0):
            answer = '''Ваши тесты:
(id, test name)

'''
            for test in tests:
                answer += f'''    {test[0]}) {test[1]}
'''
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест друга', row_width=1)
            await bot.send_message(message.chat.id, answer, reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест друга', row_width=1)
            await bot.send_message(message.chat.id, 'Вы ранее не создавали тесты', reply_markup=markup)
    
    elif (message.text == 'Пройти тест друга' and message.from_user.id not in creators and message.from_user.id not in testers):
        testers.add(message.from_user.id)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест друга', row_width=1)
        await bot.send_message(message.chat.id, 'Не понял вас', reply_markup=markup)

asyncio.run(bot.polling())