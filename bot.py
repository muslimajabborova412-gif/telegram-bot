import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router # Ин бояд бошад
from scheduler import scheduler_task
from aiohttp import web

# ... (қисми боқимондаи коди `bot.py`, ки қаблан дода будам)
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router) # Ин хат барои кор кардани /start ҳатмист!
    
    # ...
    await dp.start_polling(bot)
