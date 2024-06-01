import telebot
from telebot import types

from src.helper import helpers
from src.config import TOKEN
from src import writting_repository as wr

bot = telebot.TeleBot(TOKEN)

markup_start = types.InlineKeyboardMarkup(row_width=2)
item_report = types.InlineKeyboardButton(text = '❓ report', callback_data = 'report')
item_start = types.InlineKeyboardButton(text = '✅ start', callback_data ='start')
markup_start.add(item_report, item_start)

markup_back = types.InlineKeyboardMarkup(row_width=1)
item_back = types.InlineKeyboardButton(text = '↩️ please, back', callback_data = 'back')
markup_back.add(item_back)

def mh_main():
    print(helpers.debug_msg('mh', 'start'))
    wr.wr_main()
    mh_bot()

def mh_bot():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hi! My name is Sable 🦅, I am your personal trading mentor. I can predict where the market will go!', reply_markup=markup_start)
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.message:
            if call.data == 'report':
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, 'Report', reply_markup=markup_back)
            elif call.data == 'start':
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, 'Wow, you\'re brave! Well, look what I can say, judging by my data, the market will go up! ⬆️', reply_markup=markup_back)
            elif call.data == 'back':
                bot.delete_message(call.message.chat.id, call.message.id)
                start_message(call.message)
    
    bot.polling(none_stop=True, interval=0)