import asyncio
from aiogram import Bot
from config import CHANNEL_USERNAME

async def scheduler_task(bot: Bot):
    while True:
        try:
            # 1. Рекламаи канал
            await bot.send_message(chat_id=CHANNEL_USERNAME, text="📢 Ба канали мо обуна шавед: @English_Books_send")
            await asyncio.sleep(10) # 10 сония таваққуф

            # 2. Дарс дар бораи замонҳо
            await bot.send_message(chat_id=CHANNEL_USERNAME, text="⏰ **Замони имрӯза:** Present Simple. Барои одатҳо истифода мешавад.")
            await asyncio.sleep(10)

            # 3. Тест
            await bot.send_poll(chat_id=CHANNEL_USERNAME, question="What is your name?", options=["I am A", "My name is A"], type="quiz", correct_option_id=1)
            
            # Ҳамагӣ ҳар 24 соат (86400 сония) як бор ирсол мешавад
            await asyncio.sleep(86400) 
        except Exception as e:
            print(f"Хатогӣ: {e}")
            await asyncio.sleep(60)
