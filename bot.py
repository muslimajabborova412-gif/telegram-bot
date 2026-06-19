from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)
bot = Bot(TOKEN)

# Танзими Webhook
async def setup_webhook():
    await bot.set_webhook(url="https://NOMIN-BOTI-TUT.onrender.com/" + TOKEN)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    # Ин ҷо паёмҳо аз Telegram меоянд
    return "ok"

if __name__ == '__main__':
    # Дар ин ҷо бояд Webhook фаъол шавад
    app.run(port=8080)
