import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from scheduler import scheduler_task
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Илова кардани веб-сервер барои Render (ин хатогии портро нест мекунад)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    
    asyncio.create_task(scheduler_task(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
