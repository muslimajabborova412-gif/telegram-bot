from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Салом
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Салом! Ман боти омӯзиши англисӣ ҳастам. Чӣ саволе доред?")

# Ҷавоб ба саволҳо
@router.message()
async def echo_handler(message: Message):
    text = message.text.lower()
    
    if "goal" in text:
        await message.answer("Goal — маънояш 'ҳадаф' ё 'мақсад' аст.")
    elif "present simple" in text:
        await message.answer("Present Simple барои одатҳо истифода мешавад: Subject + V1(s/es).")
    else:
        await message.answer("Ин саволро ҳоло намедонам, аммо дар оянда ҳатман меомӯзам!")
