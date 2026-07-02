import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"

def get_unit_data(book_file, unit_number):
    if not os.path.exists(book_file):
        return []
    words = []
    with open(book_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(';')
            # Агар дар файл рақами юнит бо рақами интихобшуда рост ояд
            if len(parts) >= 4 and parts[0] == str(unit_number):
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
    # Юнитҳо аз 1 то 30
    keyboard = [[InlineKeyboardButton(f"Юнит {i}", callback_data=f"{book}_u{i}")] for i in range(1, 31)]
    await query.edit_message_text(f"Юнит-ро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

async def unit_callback(update, context):
    query = update.callback_query
    await query.answer()
    # Гирифтани номи файл ва рақами юнит
    parts = query.data.split('_u')
    book_file = f"{parts[0]}.txt"
    unit_num = parts[1]
    
    words = get_unit_data(book_file, unit_num)
    
    if not words:
        await query.message.reply_text(f"Дар ин юнит калимаҳо ёфт нашуданд. (Файли {book_file}-ро тафтиш кунед, оё дар он барои юнити {unit_num} маълумот ҳаст?)")
        return

    for item in words:
        await query.message.reply_text(f"🔹 {item['word']} — {item['trans']}\n📝 Мисол: {item['ex']}")

if __name__ == '__main__':
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(book_callback, pattern=r'^book[12]$'))
    app_bot.add_handler(CallbackQueryHandler(unit_callback, pattern=r'^book[12]_u\d+$'))
    
    print("Бот фаъол шуд...")
    app_bot.run_polling()
