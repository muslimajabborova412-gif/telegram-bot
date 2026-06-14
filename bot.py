import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Танзими Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Функсияҳои бот
def load_words(file_path):
    words = []
    if not os.path.exists(file_path): return None
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) == 4:
                words.append({'unit': parts[0], 'word': parts[1], 'translation': parts[2], 'example': parts[3]})
    return words

async def book_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name, book_name):
    words = load_words(file_name)
    if not words:
        await update.message.reply_text("Файл ёфт нашуд!")
        return
    
    # Интихоби тасодуфӣ
    word_obj = random.choice(words)
    response = (f"📚 {book_name}\n📖 Юнит: {word_obj['unit']}\n🔤 Калима: {word_obj['word']}\n🇺🇿 {word_obj['translation']}\n📝 Мисол: {word_obj['example']}")
    await update.message.reply_text(response)

async def book1(update, context): await book_handler(update, context, 'book1.txt', 'Китоби 1')
async def book2(update, context): await book_handler(update, context, 'book2.txt', 'Китоби 2')

def run_bot():
    token = os.getenv('BOT_TOKEN')
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('book1', book1))
    application.add_handler(CommandHandler('book2', book2))
    application.run_polling()

if __name__ == '__main__':
    # Оғози бот дар як риштаи алоҳида
    threading.Thread(target=run_bot).start()
    # Оғози Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
