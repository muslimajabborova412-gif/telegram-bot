import asyncio
from aiogram import Bot
from config import CHANNEL_USERNAME

async def scheduler_task(bot: Bot):
    while True:
        try:
            # Ин ҷо метавонед ҳар гуна маълумот фиристед
            message = "📚 **Китоби имрӯза:** Барои зеркашӣ ба канал обуна шавед!"
            await bot.send_message(chat_id=CHANNEL_USERNAME, text=message)
            
            # 86400 сония = 24 соат. Бот ҳар рӯз як бор пост мекунад.
            await asyncio.sleep(86400) 
        except Exception as e:
            print(f"Хатогӣ дар scheduler: {e}")
            await asyncio.sleep(60) # Агар хато шавад, 1 дақиқа интизор мешавад
