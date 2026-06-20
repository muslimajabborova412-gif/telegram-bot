import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from gtts import gTTS

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

app_bot = ApplicationBuilder().token(TOKEN).build()

# Менюи асосӣ: Интихоби китоб
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Салом! Лутфан китобро интихоб кунед:", reply_markup=reply_markup)

# Интихоби юнитҳо
async def book_callback(update, context):
    query = update.callback_query
    await query.answer()
    
    # Ин ҷо мо тугмаҳоро барои 30 юнит месозем
    keyboard = []
    for i in range(1, 31):
        keyboard.append([InlineKeyboardButton(f"Юнит {i}", callback_data=f"{query.data}_u{i}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Шумо {query.data}-ро интихоб кардед. Юнитҳоро интихоб кунед:", reply_markup=reply_markup)

# Коркарди юнит ва фиристодани луғат бо аудио
async def unit_callback(update, context):
    query = update.callback_query
    await query.answer()
    
    # Маълумот дар бораи юнит (ин ҷо бояд аз файлҳо хонда шавад)
    # Масалан: 'book1_u1'
    unit_info = query.data 
    
    # Барои мисол, як луғат:
    word = "Abandon"
    translation = "Тарк кардан"
    example = "He abandoned his car."
    
    # 1. Фиристодани матн
    await query.message.reply_text(f"🔹 {word} — {translation}\n\n📝 Мисол: {example}")
    
    # 2. Сохтани аудио (gTTS)
    tts = gTTS(text=f"{word}. {example}", lang='en', slow=True)
    tts.save("audio.mp3")
    
    # 3. Фиристодани аудио
    with open("audio.mp3", "rb") as audio:
        await query.message.reply_voice(voice=audio)

app_bot.add_handler(CommandHandler('start', start))
app_bot.add_handler(CallbackQueryHandler(book_callback, pattern='^book[12]$'))
app_bot.add_handler(CallbackQueryHandler(unit_callback, pattern='^book[12]_u\d+$'))

# ... (қисми Webhook ва Flask мисли пешина)
