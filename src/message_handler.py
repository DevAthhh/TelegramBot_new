import telebot

from src.helper import helpers
from src.config import TOKEN
from src import writting_repository as wr

bot = telebot.TeleBot(TOKEN)

markups.    

def mh_main():
    print(helpers.debug_msg('mh', 'start'))
    wr.wr_main()
    mh_bot()

def mh_bot():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hi! My name is Sable 🦅, I am your personal trading mentor. I can predict where the market will go!')
    
    bot.polling(none_stop=True, interval=0)