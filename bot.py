import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from scheduler import scheduler_task

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # scheduler_task дар замина кор мекунад
    asyncio.create_task(scheduler_task(bot))
    
    print("Бот ба кор даромад...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
