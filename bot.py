import os
import random
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Сервер барои Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Функсия барои калимаҳо
def get_random_word(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            line = random.choice(lines)
            parts = line.strip().split(';')
            if len(parts) == 4:
                return f"📖 Юнит: {parts[0]}\n🔤 Калима: {parts[1]}\n🇺🇿 Тарҷума: {parts[2]}\n📝 Мисол: {parts[3]}"
    except:
        return "Хатогӣ: Файл ёфт нашуд."

# Командаҳо
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Салом! Барои гирифтани калима /book1 ё /book2 нависед.")

async def book1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_random_word('book1.txt'), parse_mode='Markdown')

async def book2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_random_word('book2.txt'), parse_mode='Markdown')

if __name__ == '__main__':
    Thread(target=run_web).start()
    
    # ТОКЕНИ ХУДРО ИН ҶО ГУЗОР
    TOKEN = "8201016798:AAEJMbrNKdnoIoUxZUsUUKcdbcOclY1pCQM"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('book1', book1))
    application.add_handler(CommandHandler('book2', book2))
    
    application.run_polling()
