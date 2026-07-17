import asyncio
from aiogram import Bot, Dispatcher
from handlers import router

# Токени боти худро дар ин ҷо гузоред
TOKEN = "8201016798:AAEgvMTpYZTZ5uTQC1qtyt0mW5u_D3Tjp8Y"
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # Пайваст кардани роутер
    dp.include_router(router)
    
    # Оғози бот
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
