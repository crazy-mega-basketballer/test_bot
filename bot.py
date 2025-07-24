import asyncio
import requests
import time
from telebot.async_telebot import AsyncTeleBot, types
from proverka import *
from sql import *
from test_create import *
from passing_test import *


PATH = 'C:\\Users\\basda\\OneDrive\\Рабочий стол\\token.txt'
TOKEN = open(PATH).readline()
requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1').json()

bot = AsyncTeleBot(TOKEN)

async def send(id, text):
    await bot.send_message(id, text)

creators = set()
testers = {}

@bot.message_handler(commands=['start'])
async def welcome(message):
    start(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест', row_width=1)
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
            markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест', row_width=1)
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
            markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест', row_width=1)
            await bot.send_message(message.chat.id, answer, reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест', row_width=1)
            await bot.send_message(message.chat.id, 'Вы ранее не создавали тесты', reply_markup=markup)
    
    elif (message.text == 'Пройти тест' and message.from_user.id not in creators and message.from_user.id not in testers):
        testers.update({message.from_user.id : {
            'test_id' : 0,
            'start' : 0, 
            'end' : 0
        }})
        await bot.send_message(message.chat.id, 'Введите id теста, который хотите пройти:')

    elif (message.text != 'Назад' and message.from_user.id in testers):
        if (testers[message.from_user.id]['test_id'] == 0):
            test = select('tests', f'name', f'test_id = {message.text}')
            print(test)
            if len(test) == 1:
                testers[message.from_user.id]['test_id'] = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add('Да', 'Нет', 'Назад', row_width=1)
                await bot.send_message(message.chat.id, f'Хотите пройти тест "{test[0][0]}"', reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add('Назад', row_width=1)
                await bot.send_message(message.chat.id, 'Нету такого🖕, но ты можешь попробовать еще раз🥺', reply_markup=markup)

        else:
            if (testers[message.from_user.id]['start'] == 0 and message.text == 'Да'):
                testers[message.from_user.id]['start'] == int(time.time())
                await bot.send_message(message.chat.id, 'Супер, тогда начнем!')
                passing(message.chat.id, testers[message.from_user.id]['test_id'])
            elif (testers[message.from_user.id]['start'] == 0 and message.text == 'Нет'):
                testers.pop(message.chat.id, None)
                await bot.send_message(message.chat.id, 'Ну и похуй мне, я даже не обиделся')
            else:
                if passing(message.chat.id, testers[message.from_user.id]['test_id']):
                    testers.pop(message.chat.id, None)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Создать тест', 'Мои тесты', 'Друзья', 'Пройти тест', row_width=1)
        if (message.text == 'Назад'):
            await bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup)
            testers.pop(message.chat.id, None)
        else:
            await bot.send_message(message.chat.id, 'Не понял вас', reply_markup=markup)

asyncio.run(bot.polling())