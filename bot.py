import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Танзими логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Гирифтани токенҳо аз Render Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("GEMINI_API_KEY")

# Танзими Gemini AI (модели gemini-pro барои устуворӣ)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Дархост ба AI
        response = model.generate_content(user_text)
        # Фиристодани ҷавоб
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Хатогӣ дар AI: {e}")
        await update.message.reply_text("Бубахшед, дар ҷавоб додан хатогӣ рух дод.")

if __name__ == '__main__':
    # Инициализатсияи бот
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Қабул кардани ҳамаи паёмҳои матнӣ
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот фаъол шуд...")
    app.run_polling()
