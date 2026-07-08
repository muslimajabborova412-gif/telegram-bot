from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Луғати китобҳо
BOOKS = {
    "b2": {"file": "4000 Essential English words 2.pdf", "name": "Essential English Words 2"},
    "b3": {"file": "4000 Essential English words 3.pdf", "name": "Essential English Words 3"},
    # Илова кунед барои дигарон
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Китоби 2", callback_data="b2")],
        [InlineKeyboardButton("Китоби 3", callback_data="b3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Китоби худро интихоб кунед:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    book_id = query.data
    book = BOOKS.get(book_id)
    
    if book:
        # Ин ҷо бот PDF-ро ҳамчун документ мефиристад
        # caption - ин матнест, ки зери файл меояд
        await context.bot.send_document(
            chat_id=query.message.chat_id, 
            document=open(book['file'], 'rb'),
            caption=f"Ин китоби '{book['name']}' аст."
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token("8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
