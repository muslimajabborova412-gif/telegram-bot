import os
import random
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# Танзими сервери хурд барои Render (Web Service)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Функсия барои хондани калимаҳо аз файл
def get_random_word(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            line = random.choice(lines)
            parts = line.strip().split(';')
            if len(parts) == 4:
                return f"📖 Юнит: {parts[0]}\n🔤 Калима: {parts[1]}\n🇺🇿 Тарҷума: {parts[2]}\n📝 Мисол: {parts[3]}"
    except Exception as e:
        return "Хатогӣ дар хондани файл."

# Командаҳо барои ҳарду китоб
async def book1(update, context):
    word = get_random_word('book1.txt')
    await update.message.reply_text(f"📚 **Китоби 1:**\n\n{word}", parse_mode='Markdown')

async def book2(update, context):
    word = get_random_word('book2.txt')
    await update.message.reply_text(f"📚 **Китоби 2:**\n\n{word}", parse_mode='Markdown')

if __name__ == '__main__':
    # 1. Серверро дар алоҳидагӣ сар медиҳем
    Thread(target=run_web).start()

    # 2. Танзими бот
    TOKEN = "8201016798:AAEJMbrNKdnoIoUxZUsUUKcdbcOclY1pCQM" # Токени дурустро дар ин ҷо гузор
    application = ApplicationBuilder().token(TOKEN).build()
    
    # 3. Илова кардани командаҳо
    application.add_handler(CommandHandler('book1', book1))
    application.add_handler(CommandHandler('book2', book2))
    
    application.run_polling()
