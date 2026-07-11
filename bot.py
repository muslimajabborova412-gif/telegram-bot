import asyncio
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from scheduler import scheduler_task
from aiohttp import web

async def health_check(request):
    return web.Response(text="Bot is running!")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # 1. Задани веб-сервер барои Render
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # 2. Оғози автопостинг ва бот
    asyncio.create_task(scheduler_task(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
