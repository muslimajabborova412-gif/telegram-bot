from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Танҳо ин ҷо токени худро нависед
BOT_TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"

PDF_FILE_NAME = "4000 Essential English words 2.pdf"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📥 Гирифтани китоби 2", callback_data="send_file")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Салом! Барои гирифтани китоб тугмаро пахш кунед:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "send_file":
        # Санҷиши мавҷуд будани файл
        if os.path.exists(PDF_FILE_NAME):
            await context.bot.send_document(
                chat_id=query.message.chat_id, 
                document=open(PDF_FILE_NAME, 'rb'),
                caption="📚 Ин аст китоби '4000 Essential English Words 2'"
            )
        else:
            await query.message.reply_text("Хатогӣ: Файли PDF ёфт нашуд!")

if __name__ == '__main__':
    # Бот бо токени дар боло навишташуда сохта мешавад
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот фаъол шуд...")
    app.run_polling()
