import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Танзимоти лог
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 8080))

app = Flask(__name__)

# Истифодаи Application барои Webhook
application = Application.builder().token(TOKEN).build()

# Командаҳо
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот фаъол аст!")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    # Телеграм маълумотро ба ин ҷо мефиристад
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.bot.process_update(update)
    return "ok", 200

@app.route('/')
def index():
    return "Bot is running via Webhook!"

if __name__ == '__main__':
    # Webhook-ро ба Телеграм пайваст мекунем
    # Дар ин ҷо 'https://nomi-loyhai-shumo.onrender.com' -ро нависед
    webhook_url = f"https://telegram-bot-worker.onrender.com/{TOKEN}"
    application.bot.set_webhook(webhook_url)
    
    app.run(host='0.0.0.0', port=PORT)
