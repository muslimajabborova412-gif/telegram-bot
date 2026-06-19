import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Сохтани Loop барои Render
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Танзими бот
app_bot = ApplicationBuilder().token(TOKEN).build()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Қабули паёмҳо аз Telegram
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, app_bot.bot)
    asyncio.run_coroutine_threadsafe(app_bot.update_queue.put(update), loop)
    return "ok", 200

if __name__ == '__main__':
    # Webhook-ро худамон ба Telegram танзим мекунем
    bot = Bot(TOKEN)
    webhook_url = "https://telegram-bot-9thf.onrender.com/webhook"
    loop.run_until_complete(bot.set_webhook(url=webhook_url))
    
    # Оғози сервер
    app.run(host='0.0.0.0', port=10000)
