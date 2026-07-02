import os
import asyncio
import logging
import threading
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from gtts import gTTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
WEBHOOK_URL = "https://telegram-bot-9thf.onrender.com/webhook"

app = Flask(__name__)
# Loop-и асосиро мегирем
loop = asyncio.new_event_loop()

app_bot = ApplicationBuilder().token(TOKEN).build()

# ... (функсияҳои start, book_callback, unit_callback-и шумо) ...
# ЭЗОҲ: Ҳамаи Handler-ҳоро ҳамин ҷо илова кунед!
app_bot.add_handler(CommandHandler('start', start))
app_bot.add_handler(CallbackQueryHandler(book_callback, pattern=r'^book[12]$'))
app_bot.add_handler(CallbackQueryHandler(unit_callback, pattern=r'^book[12]_u\d+$'))

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    if json_data:
        update = Update.de_json(json_data, app_bot.bot)
        # Истифодаи run_coroutine_threadsafe барои пешгирии хатои Event loop
        asyncio.run_coroutine_threadsafe(app_bot.process_update(update), loop)
    return "ok", 200

if __name__ == '__main__':
    # Омодасозии бот дар Loop-и асосӣ
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.initialize())
    loop.run_until_complete(app_bot.bot.set_webhook(url=WEBHOOK_URL))
    
    # Иҷрои бот дар як Thread-и алоҳида, то ки Flask ва Бот халал нарасонанд
    threading.Thread(target=app_bot.run_polling, daemon=True).start() # Агар лозим бошад
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)
