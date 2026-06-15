import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

# 1. Танзими Flask барои қонеъ кардани Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Render порти 10000-ро истифода мебарад
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# 2. Коди аслии бот
async def start(update, context):
    await update.message.reply_text("Салом! Бот кор мекунад.")

if __name__ == '__main__':
    # Flask-ро дар паси парда ба кор меандозем
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Ботро бо polling ба кор меандозем
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Бот ва Flask ба кор даромаданд...")
    application.run_polling()
