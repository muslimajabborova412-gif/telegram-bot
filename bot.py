import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Ботро омода мекунем
app_bot = ApplicationBuilder().token(TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Салом! Бот кор мекунад! ✅")

app_bot.add_handler(CommandHandler('start', start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Қабули паём аз Telegram
    data = request.get_json(force=True)
    update = Update.de_json(data, app_bot.bot)
    
    # Иҷрои паём
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.process_update(update))
    return "ok", 200

if __name__ == '__main__':
    # Webhook-ро дар Telegram танзим мекунем
    bot = Bot(TOKEN)
    webhook_url = "https://telegram-bot-9thf.onrender.com/webhook"
    
    # Инро дар браузер кушоед, агар бот кор накунад:
    # https://api.telegram.org/bot8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0/setWebhook?url=https://telegram-bot-9thf.onrender.com/webhook
    
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
