import os
import random
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Сервери Flask барои Render (Web Service)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Функсияи гирифтани калимаҳои як юнит
def get_unit_words(book_file, unit_num):
    words = []
    try:
        with open(book_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) == 4 and parts[0] == str(unit_num):
                    words.append(f"🔤 **{parts[1]}**\n🇺🇿 {parts[2]}\n📝 {parts[3]}")
    except:
        return []
    return words

# Менюи асосӣ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("📚 4000 Essential English Words 2", callback_data='book2')]
    ]
    await update.message.reply_text("Хуш омадед! Китобро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

# Идоракунии тугмаҳо
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ['book1', 'book2']:
        context.user_data['book'] = f"{query.data}.txt"
        # Сохтани 30 тугма барои юнитҳо
        keyboard = [[InlineKeyboardButton(f"Unit {i}", callback_data=f"unit_{i}")] for i in range(1, 31)]
        await query.edit_message_text(f"Юнитро аз {query.data} интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('unit_'):
        unit_num = query.data.split('_')[1]
        book_file = context.user_data.get('book')
        words = get_unit_words(book_file, unit_num)
        
        if words:
            await query.edit_message_text(f"📖 Калимаҳои Юнити {unit_num}:\n\n" + "\n\n".join(words), parse_mode='Markdown')
        else:
            await query.edit_message_text("Калимаҳо ёфт нашуданд ё юнит холӣ аст.")

if __name__ == '__main__':
    Thread(target=run_web).start()
    
    TOKEN = "8201016798:AAEJMbrNKdnoIoUxZUsUUKcdbcOclY1pCQM"
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(button))
    
    app_bot.run_polling()
