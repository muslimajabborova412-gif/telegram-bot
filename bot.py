import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ⚠️ ТОКЕНИ БОТИ ХУДРО АЗ BOTFATHER ДАР БАЙНИ СИТАТАҲО ГУЗОР
TOKEN = '8996159898:AAEFani_soW7FmDlf2Uvrga0ruJKWfN9r64'

# Сохтани Веб-Сайти Flask барои Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот фаъол аст ва кор мекунад! 🚀"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Салом! Боти ту дар Render бомуваффақият кор карда истодааст! 🚀')

def run_flask():
    # Портеро, ки Render медиҳад, мехонад
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def main() -> None:
    # 1. Сар кардани сайт дар замина (background)
    threading.Thread(target=run_flask, daemon=True).start()

    # 2. Сар кардани худи боти Telegram
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Бот ва Веб-сервер ба кор даромаданд...")
    application.run_polling()

if __name__ == '__main__':
    main()
