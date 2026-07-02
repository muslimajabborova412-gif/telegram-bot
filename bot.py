import os
import asyncio
import logging
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from gtts import gTTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
WEBHOOK_URL = "https://telegram-bot-9thf.onrender.com/webhook"

app = Flask(__name__)

# Мо объектро месозем
app_builder = ApplicationBuilder().token(TOKEN)
app_bot = app_builder.build()

# Иловаи Handler-ҳо (инҳоро пеш аз инициализатсия илова кунед)
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    await update.message.reply_text("Китобро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

# ... (дигар функцияҳои шумо, ба монанди book_callback ва unit_callback ҳамон хел мемонанд)
app_bot.add_handler(CommandHandler('start', start))
# (Хатҳои дигари add_handler-ро ин ҷо илова кунед)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    if json_data:
        update = Update.de_json(json_data, app_bot.bot)
        # Ботро дар дохили дархост коркард мекунем
        asyncio.run(app_bot.process_update(update))
    return "ok", 200

if __name__ == '__main__':
    # Муҳим: Инициализатсияи бот
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.initialize())
    loop.run_until_complete(app_bot.bot.set_webhook(url=WEBHOOK_URL))
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
