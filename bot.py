import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Токени шумо
BOT_TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"

# Феҳристи китобҳо (Номи файлҳо бояд бо номи дар папка буда якхела бошад)
BOOKS = {
    "b1": {"file": "4000 Essential English words 1.pdf", "name": "Китоби 1"},
    "b2": {"file": "4000 Essential English words 2.pdf", "name": "Китоби 2"},
    "b3": {"file": "4000 Essential English words 3.pdf", "name": "Китоби 3"},
    "b4": {"file": "4000 Essential English words 4.pdf", "name": "Китоби 4"},
    "b5": {"file": "4000 Essential English words 5.pdf", "name": "Китоби 5"},
    "b6": {"file": "4000 Essential English words 6.pdf", "name": "Китоби 6"},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохтани тугмаҳо барои 6 китоб
    keyboard = [
        [InlineKeyboardButton("Китоби 1", callback_data="b1"), InlineKeyboardButton("Китоби 2", callback_data="b2")],
        [InlineKeyboardButton("Китоби 3", callback_data="b3"), InlineKeyboardButton("Китоби 4", callback_data="b4")],
        [InlineKeyboardButton("Китоби 5", callback_data="b5"), InlineKeyboardButton("Китоби 6", callback_data="b6")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 Салом! Китоби дилхоҳи '4000 Essential English Words'-ро интихоб кунед:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    book_id = query.data
    book = BOOKS.get(book_id)
    
    if book:
        file_path = book['file']
        if os.path.exists(file_path):
            await query.message.reply_text(f"📥 {book['name']} фиристода шуда истодааст...")
            await context.bot.send_document(
                chat_id=query.message.chat_id, 
                document=open(file_path, 'rb'),
                caption=f"Ин аст {book['name']}"
            )
        else:
            await query.message.reply_text(f"Хатогӣ: Файли '{file_path}' дар сервер ёфт нашуд.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот фаъол шуд...")
    app.run_polling()
