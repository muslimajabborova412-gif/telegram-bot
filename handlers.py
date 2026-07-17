from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Намунаи ҷавоб барои саволи мушаххас
@dp.message()
async def echo_handler(message: types.Message):
    text = message.text.lower()
    
    if "goal" in text:
        await message.answer("Goal — маънояш 'ҳадаф' аст.")
    elif "present simple" in text:
        await message.answer("Present Simple барои амалҳои такроршаванда истифода мешавад.")
    else:
        await message.answer("Саломи дубора! Барои омӯзиши англисӣ аз ман дар бораи грамматика ё калимаҳо пурсед.")
