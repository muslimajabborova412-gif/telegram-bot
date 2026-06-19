import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from gtts import gTTS

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)
app_bot = ApplicationBuilder().token(TOKEN).build()

# ... (функсияҳои get_unit_words, start, button ҳамон тавре ки буданд, бимонанд) ...

# ИН ҚИСМАТРО ДАР ПОЁНИ КОД ИВАЗ КУН:
if __name__ == '__main__':
    # 1. Loop-и нав месозем
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # 2. Webhook-ро танзим мекунем
    async def set_wh():
        bot = Bot(TOKEN)
        await bot.set_webhook(url=f"https://telegram-bot-9thf.onrender.com/{TOKEN}")
    
    loop.run_until_complete(set_wh())
    
    # 3. Серверро бо Flask оғоз мекунем
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
