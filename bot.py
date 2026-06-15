import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# 1. Танзими Flask барои Web Service (барои Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# 2. Логикаи Бот
async def start(update, context):
    await update.message.reply_text("Боти ман ҳамчун Web Service кор мекунад!")

if __name__ == '__main__':
    # Серверро дар алоҳидагӣ сар медиҳем
    Thread(target=run_web).start()

    # Токени худро дар ин ҷо боэҳтиёт иваз кун
    TOKEN = "ТОКЕНИ_ҲАҚИҚИИ_ХУДРО_ДАР_ИН_ҶО_ГУЗОР"
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    
    application.run_polling()
