import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Танзими логгинг барои дидани хатогиҳо дар Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Гирифтани токенҳо аз Render Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

# Танзими Gemini AI (модели навтарин)
genai.configure(api_key=API_KEY)
# Истифодаи gemini-1.5-flash барои ҳалли хатогии 404
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Дархост ба AI
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        # Лог кардани хатогӣ
        logging.error(f"Хатогӣ дар AI: {e}")
        # Фиристодани хатогӣ ба Telegram барои ташхис
        await update.message.reply_text(f"Хатогӣ рух дод: {str(e)}")

if __name__ == '__main__':
    if not BOT_TOKEN or not API_KEY:
        print("Хатогӣ: BOT_TOKEN ё GEMINI_API_KEY танзим нашудаанд!")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("Бот фаъол шуд...")
        app.run_polling()
