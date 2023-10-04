import telebot

TOKEN = '6667553537:AAFc6aweh53KVADf9MEJ9x-39Gi7FJV34lo'

bot = telebot.TeleBot(TOKEN)


def start_bot():
    bot.polling()