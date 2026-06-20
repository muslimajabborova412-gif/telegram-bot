import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from gtts import gTTS

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Инициализатсияи бот
app_bot = ApplicationBuilder().token(TOKEN).build()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(app_bot.initialize())

# Функсияи хондани файл
def get_unit_data(book_file, unit_number):
    words = []
    if not os.path.exists(book_file): return words
    with open(book_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) == 4 and parts[0] == str(unit_number):
                words.append({"word": parts[1], "trans": parts[2], "ex": parts[3]})
    return words

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    await update.message.reply_text("Китобро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

async def book_callback(update, context):
    query = update.callback_query
    await query.answer()
    book = query.data
    keyboard = [[InlineKeyboardButton(f"Юнит {i}", callback_data=f"{book}_u{i}")] for i in range(1, 31)]
    await query.edit_message_text("Юнит-ро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

async def unit_callback(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data.split('_u')
    book_file = f"{data[0]}.txt"
    unit_num = data[1]
    
    words = get_unit_data(book_file, unit_num)
    
    if not words:
        await query.message.reply_text("Маълумот барои ин юнит ёфт нашуд.")
        return

    for item in words:
        await query.message.reply_text(f"🔹 {item['word']} — {item['trans']}\n📝 Мисол: {item['ex']}")
        tts = gTTS(text=f"{item['word']}. {item['ex']}", lang='en', slow=True)
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as audio:
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
