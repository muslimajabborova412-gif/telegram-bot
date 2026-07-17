import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import router

# Агар дар Render 'Environment Variable' илова карда бошӣ, аз ин ҷо мехонад
TOKEN = os.getenv("BOT_TOKEN") 

async def main():
    if not TOKEN:
        print("Хатогӣ: Токен ёфт нашуд!")
        return
        
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)
    
    print("Бот ба кор даромад...")
    # Иловаи drop_pending_updates барои бартараф кардани ConflictError
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
