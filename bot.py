import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

# Сервери хурди Flask барои қонеъ кардани Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Render порти 10000-ро истифода мебарад
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    # Flask-ро дар як поток (thread) алоҳида ба кор меандозем
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Ботро бо polling ба кор меандозем
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Бот кор мекунад!")))
    
    print("Бот ва Flask ба кор даромаданд...")
    application.run_polling()
