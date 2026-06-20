import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# Сохтани бот
app_bot = ApplicationBuilder().token(TOKEN).build()

# Ҳандлери /start
async def start(update, context):
    await update.message.reply_text("Бот бо муваффақият кор мекунад! ✅")

app_bot.add_handler(CommandHandler('start', start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Қабули паём аз Telegram
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, app_bot.bot)
    
    # Иҷрои паём
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app_bot.process_update(update))
    return "ok", 200

# Ин барои пешгирии 404 дар саҳифаи асосӣ
@app.route('/')
def index():
    return "Bot is active!"

if __name__ == '__main__':
    # Оғози сервер
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
