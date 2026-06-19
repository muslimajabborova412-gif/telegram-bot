import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)
bot = Bot(TOKEN)

# Мо як "Application" месозем, аммо онро бо 'run_polling' не, балки бо Webhook мепайвастем
app_bot = ApplicationBuilder().token(TOKEN).build()
# Илова кардани Handler-ҳо (start ва button)
# app_bot.add_handler(...) - дар ин ҷо ҳамон кодҳои худро илова кун

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot.bot)
    app_bot.update_queue.put(update)
    return "ok"

if __name__ == '__main__':
    # Webhook-ро фаъол мекунем
    bot.set_webhook(url=f"https://NOMIN-BOTI-TUT.onrender.com/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
