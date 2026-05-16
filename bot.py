import os
import asyncio
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ⚠️ ТОКЕНИ БОТИ ХУДРО АЗ BOTFATHER ДАР БАЙНИ СИТАТАҲО ГУЗОР
TOKEN = '8996159898:AAEFani_soW7FmDlf2Uvrga0ruJKWfN9r64'

# Ин қисм барои он аст, ки Render ботро хомӯш накунад
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    handler = SimpleHTTPRequestHandler
    with TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Веб-сервер дар порти {port} сар шуд...")
        httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Салом! Боти ту дар Render бомуваффақият кор карда истодааст! 🚀')

def main() -> None:
    # Ба кор даровардани веб-сервер дар замина (background)
    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Сохтани бот бо китобхонаи аслии python-telegram-bot
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Бот ба кор даромад...")
    application.run_polling()

if __name__ == '__main__':
    main()
