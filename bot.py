import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from scheduler import scheduler_task

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Оғози scheduler дар замина (background)
    asyncio.create_task(scheduler_task(bot))
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
