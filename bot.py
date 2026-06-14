import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ин ҷо бот бо шумо гап мезанад
    await update.message.reply_text("Салом! Бот омода аст. Барои хондани китобҳо метавонед пурсед.")

if __name__ == '__main__':
    # Ин усул барои Background Worker дар Render беҳтарин аст
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("Бот оғоз шуд...")
    application.run_polling()
