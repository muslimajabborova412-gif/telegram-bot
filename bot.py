import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Ботро бо ApplicationBuilder месозем
app_bot = ApplicationBuilder().token(TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Бот бо муваффақият пайваст шуд! ✅")

app_bot.add_handler(CommandHandler('start', start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Ин ҷо мо паёмро аз Telegram мегирем ва ба Application мефиристем
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app_bot.bot)
    
    # Иҷрои паём дар background
    asyncio.run_coroutine_threadsafe(app_bot.process_update(update), asyncio.get_event_loop())
    return "ok", 200

# Роҳи асосӣ барои санҷиш, ки бот "зинда" аст
@app.route('/')
def index():
    return "Бот кор мекунад!"

if __name__ == '__main__':
    # Webhook-ро худамон маҷбурӣ танзим мекунем
    bot = Bot(TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.set_webhook(url="https://telegram-bot-9thf.onrender.com/webhook"))
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
