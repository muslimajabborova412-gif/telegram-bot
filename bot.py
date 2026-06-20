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
    await update.message.reply_text("Салом! Бот кор мекунад! ✅")

app_bot.add_handler(CommandHandler('start', start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Ин ҷо мо паёмро аз Telegram мегирем
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app_bot.bot)
    
    # Иҷрои паём дар background бе хатогии loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.process_update(update))
    return "ok", 200

# Роҳи асосӣ барои санҷиш, ки бот "зинда" аст
@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    # Webhook-ро худамон танзим мекунем
    bot = Bot(TOKEN)
    # Истифодаи URL-и Render-и ту
    url = "https://telegram-bot-9thf.onrender.com/webhook"
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.set_webhook(url=url))
    
    # Оғози сервер дар порти 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
