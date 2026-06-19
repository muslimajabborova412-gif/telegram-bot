import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Истифодаи ApplicationBuilder барои коркарди паёмҳо
app_bot = ApplicationBuilder().token(TOKEN).build()

# Функсияи оддии ҷавоб ба /start
async def start(update, context):
    await update.message.reply_text("Салом! Бот кор мекунад! ✅")

app_bot.add_handler(CommandHandler('start', start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Қабули JSON аз Telegram
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, app_bot.bot)
    
    # Истифодаи asyncio барои иҷрои Handler-ҳо
    asyncio.run_coroutine_threadsafe(app_bot.process_update(update), asyncio.get_event_loop())
    return "ok", 200

if __name__ == '__main__':
    # Webhook-ро дар Telegram танзим мекунем
    bot = Bot(TOKEN)
    webhook_url = "https://telegram-bot-9thf.onrender.com/webhook"
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.set_webhook(url=webhook_url))
    
    # Оғози Flask
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
