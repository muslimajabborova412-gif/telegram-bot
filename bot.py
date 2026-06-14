import os
import telebot
from flask import Flask
import threading

# API TOKEN аз Render гирифта мешавад
TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Flask барои Render (барои он ки хомӯш нашавад)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Салом! Бот кор мекунад.")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    # Оғоз кардани бот дар як поток
    threading.Thread(target=run_bot).start()
    # Оғоз кардани Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
