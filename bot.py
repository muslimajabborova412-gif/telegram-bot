from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Номи файл бояд айнан ҳамин бошад
PDF_FILE_NAME = "4000 Essential English words 2.pdf"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📥 Гирифтани китоби 2", callback_data="send_file")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Салом! Барои гирифтани китоб тугмаро пахш кунед:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "send_file":
        await query.message.reply_text("Файл фиристода шуда истодааст...")
        # Фиристодани ҳамон файли PDF-е, ки шумо бор кардед
        await context.bot.send_document(
            chat_id=query.message.chat_id, 
            document=open(PDF_FILE_NAME, 'rb'),
            caption="📚 Ин аст китоби '4000 Essential English Words 2'"
        )

if __name__ == '__main__':
    # Токени боти худро ин ҷо гузоред
    BOT_TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот фаъол шуд...")
    app.run_polling()
