from telebot.async_telebot import telebot, types

PATH = 'C:\\Users\\basda\\OneDrive\\Рабочий стол\\token.txt'
TOKEN = open(PATH).readline()
bot = telebot.TeleBot(TOKEN)

def send(id, text, buttons = [], r = 1, t = 1):
    if (len(buttons) != 0 and t == 1):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for but in buttons:
            markup.add(but)
        markup.add(row_width=r)
        bot.send_message(id, text, reply_markup=markup)
    else:
        bot.send_message(id, text)