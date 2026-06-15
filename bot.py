import os
import random
from flask import Flask
from threading import Thread
from gtts import gTTS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Сервери Flask барои Render
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Функсияи гирифтани калимаҳо аз юнит
def get_unit_words(book_file, unit_num):
    words = []
    try:
        with open(book_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) == 4 and parts[0] == str(unit_num):
                    words.append(parts)
    except: return []
    return words

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    await update.message.reply_text("Китобро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update, context):
    query = update.callback_query
    await query.answer()

    if query.data in ['book1', 'book2']:
        context.user_data['book'] = f"{query.data}.txt"
        # Тугмаҳо барои 30 юнит
        keyboard = [[InlineKeyboardButton(f"Unit {i}", callback_data=f"unit_{i}")] for i in range(1, 31)]
        await query.edit_message_text("Юнитро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('unit_'):
        unit_num = query.data.split('_')[1]
        book_file = context.user_data.get('book')
        words = get_unit_words(book_file, unit_num)
        
        if words:
            await query.edit_message_text(f"📖 Юнити {unit_num}-ро омода карда истодаам...")
            for w in words:
                word_text = f"🔤 {w[1]}\n🇺🇿 {w[2]}\n📝 {w[3]}"
                await context.bot.send_message(chat_id=query.message.chat_id, text=word_text)
                
                # Сохтани аудио (калима + мисол)
                tts = gTTS(text=f"{w[1]}. {w[3]}", lang='en', slow=True)
                tts.save("speech.mp3")
                await context.bot.send_audio(chat_id=query.message.chat_id, audio=open("speech.mp3", "rb"))
        else:
            await query.edit_message_text("Дар ин юнит калима ёфт нашуд.")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.getenv("TOKEN") 
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.run_polling()
