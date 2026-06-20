import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Токени боти шумо
TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Сохтани бот бо ApplicationBuilder
app_bot = ApplicationBuilder().token(TOKEN).build()

# Инициализатсияи бот (ин қисми муҳим барои коркарди дуруст аст)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(app_bot.initialize())

# Функсияи /start
async def start(update, context):
    await update.message.reply_text("Салом! Бот бо муваффақият кор мекунад! ✅")

app_bot.add_handler(CommandHandler('start', start))

# Роҳи қабули паёмҳо тавассути Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app_bot.bot)
    
    # Иҷрои паём дар loop
    loop.run_until_complete(app_bot.process_update(update))
    return "ok", 200

# Роҳи асосӣ барои санҷиш
@app.route('/')
def index():
    return "Бот фаъол аст!"

if __name__ == '__main__':
    # Webhook-ро дар Telegram танзим мекунем
    bot = Bot(TOKEN)
    webhook_url = "https://telegram-bot-9thf.onrender.com/webhook"
    loop.run_until_complete(bot.set_webhook(url=webhook_url))
    
    # Оғози сервер дар порти Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
