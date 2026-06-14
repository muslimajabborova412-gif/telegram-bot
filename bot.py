import os
from flask import Flask
from gtts import gTTS
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Танзимот
TOKEN = os.getenv("BOT_TOKEN")
SELECT_BOOK, SELECT_UNIT = range(2)

app = Flask(__name__)

# Мантиқи оддии гирифтани луғат аз файл (тасаввур кунем, ки дар файл формат: калима - тарҷума - мисол аст)
def get_data(book_name, unit):
    # Ин ҷо шумо бояд номи файлро мувофиқи book_name муайян кунед
    # Ва файлро хонда 20 луғати он юнит-ро баргардонед
    return [("Abandon", "Тарк кардан", "He decided to abandon the project.")]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["4000 Essential English Words 1"], ["4000 Essential English Words 2"]]
    await update.message.reply_text("Лутфан китобро интихоб кунед:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return SELECT_BOOK

async def select_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['book'] = update.message.text
    await update.message.reply_text("Юнитро нависед (1-30):")
    return SELECT_UNIT

async def select_unit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unit = update.message.text
    words = get_data(context.user_data['book'], unit)
    
    for word, trans, ex in words:
        # 1. Намоиши матн
        await update.message.reply_text(f"📖 {word} - {trans}\n💬 {ex}")
        
        # 2. Сохтани аудиои калима (фақат калима)
        tts = gTTS(text=word, lang='en')
        tts.save("word.mp3")
        await update.message.reply_audio(audio=open("word.mp3", "rb"))
        os.remove("word.mp3")
        
    return ConversationHandler.END

if __name__ == '__main__':
    # Барои Render: Web Service бояд порт дошта бошад
    application = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_BOOK: [MessageHandler(filters.TEXT, select_book)],
            SELECT_UNIT: [MessageHandler(filters.TEXT, select_unit)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    
    # Render талаб мекунад, ки бот дар Web Service кор кунад
    port = int(os.environ.get("PORT", 10000))
    application.run_webhook(listen="0.0.0.0", port=port, url_path=TOKEN, webhook_url=f"https://telegram-bot-hnav.onrender.com/{TOKEN}")
