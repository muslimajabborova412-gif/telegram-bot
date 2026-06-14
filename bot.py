import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Танзимоти логҳо
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Гирифтани токен аз Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
# URL-и боти шумо дар Render (онро аз панели Render гиред)
WEBHOOK_URL = "https://telegram-bot-hnav.onrender.com"

app = Flask(__name__)

# Сохтани бот
bot = Bot(token=TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Салом! Хуш омадед ба боти расмии Абдурраҳим! 🚀")

# Танзими Application
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Бот кор мекунад!", 200

if __name__ == "__main__":
    # Насб кардани Webhook ҳангоми оғоз
    import asyncio
    asyncio.run(bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}"))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
