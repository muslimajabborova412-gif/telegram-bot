import asyncio
from aiogram import Bot
from config import CHANNEL_USERNAME

async def send_daily_post(bot: Bot):
    # Ин ҷо матни дарс ё тести худро менависед
    lesson_text = "📚 **Дарси имрӯза:** Биёед имрӯз замони Present Simple-ро такрор кунем..."
    
    # Ирсол ба канал
    await bot.send_message(chat_id=CHANNEL_USERNAME, text=lesson_text)

async def scheduler_task(bot: Bot):
    while True:
        # Ин ҷо вақтро танзим мекунем (масалан, ҳар 24 соат - 86400 сония)
        await send_daily_post(bot)
        await asyncio.sleep(86400)
