import telebot

bot = telebot.TeleBot('7300492927:AAF6BOO36Z_OyRRBXlNu-JqsaBK5PQqNP6Y')

@bot.message_handler(content_types=['text'])
def start_message(message):
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)