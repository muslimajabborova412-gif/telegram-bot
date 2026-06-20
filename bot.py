import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from gtts import gTTS

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

app_bot = ApplicationBuilder().token(TOKEN).build()

# Инициализатсияи бот
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(app_bot.initialize())

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Салом! Китоби дилхоҳро интихоб кунед:", reply_markup=reply_markup)

async def book_callback(update, context):
    query = update.callback_query
    await query.answer()
    keyboard = []
    for i in range(1, 31):
        keyboard.append([InlineKeyboardButton(f"Юнит {i}", callback_data=f"{query.data}_u{i}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Шумо {query.data}-ро интихоб кардед. Юнитҳо:", reply_markup=reply_markup)

async def unit_callback(update, context):
    query = update.callback_query
    await query.answer()
    
    # Мисол барои луғат (барои 4000 калима, инро аз файлҳои txt-и худ хонед)
    word, trans, ex = "Abandon", "Тарк кардан", "He abandoned his car."
    
    await query.message.reply_text(f"🔹 {word} — {trans}\n\n📝 Мисол: {ex}")
    
    # Сохтани аудио бо суръати паст
    tts = gTTS(text=f"{word}. {ex}", lang='en', slow=True)
    tts.save("audio.mp3")
    with open("audio.mp3", "rb") as audio:
        await query.message.reply_voice(voice=audio)

app_bot.add_handler(CommandHandler('start', start))
app_bot.add_handler(CallbackQueryHandler(book_callback, pattern=r'^book[12]$'))
app_bot.add_handler(CallbackQueryHandler(unit_callback, pattern=r'^book[12]_u\d+$'))

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app_bot.bot)
    loop.run_until_complete(app_bot.process_update(update))
    return "ok", 200

if __name__ == '__main__':
    bot = Bot(TOKEN)
    webhook_url = "https://telegram-bot-9thf.onrender.com/webhook"
    loop.run_until_complete(bot.set_webhook(url=webhook_url))
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
