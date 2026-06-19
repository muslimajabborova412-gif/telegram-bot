import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

# 1. Loop-ро маҷбуран дар аввал месозем
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Ботро бо ҳамин loop омода мекунем
app_bot = ApplicationBuilder().token(TOKEN).build()

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        json_update = request.get_json(force=True)
        update = Update.de_json(json_update, app_bot.bot)
        # 3. Истифодаи run_coroutine_threadsafe барои коркарди бехатар
        asyncio.run_coroutine_threadsafe(app_bot.update_queue.put(update), loop)
        return "ok", 200

if __name__ == '__main__':
    # 4. Танзими Webhook
    async def set_webhook():
        bot = Bot(TOKEN)
        await bot.set_webhook(url="https://telegram-bot-9thf.onrender.com/webhook")
    
    loop.run_until_complete(set_webhook())
    
    # 5. Оғози Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
