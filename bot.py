import os
import asyncio
from aiohttp import web
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from database import init_db
from handlers import start_command, button_callback_handler, text_handler
from scheduler import start_scheduler

# Функсия барои фиреб додани Render (банд кардани Порт)
async def handle_web(request):
    return web.Response(text="Бот фаъол аст!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render худаш порстро ба таври автоматӣ медиҳад
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер дар форти {port} оғоз шуд.")

def main():
    # 1. Сар кардани Базаи маълумот
    init_db()
    
    # 2. Сохтани лоиҳаи Бот бо JobQueue
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # 3. Пайваст кардани командаҳо ва тугмаҳо
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_callback_handler, pattern="^check_subscription$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    # 4. Фаъол кардани автопостинг
    start_scheduler(application)
    
    # 5. Идораи кор давомдор (Асинхронӣ)
    loop = asyncio.get_event_loop()
    
    # Ба кор андохтани веб-сервер барои Render
    loop.create_task(start_web_server())
    
    # Ба кор андохтани бот
    print("Бот бомуваффақият фаъол шуд...")
    application.run_polling()

if __name__ == "__main__":
    main()
