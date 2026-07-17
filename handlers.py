from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Салом! Ман боти омӯзиши англисӣ ҳастам. Чӣ саволе доред?")

@router.message()
async def echo_handler(message: Message):
    text = message.text.lower()
    if "goal" in text:
        await message.answer("Goal — маънояш 'ҳадаф' ё 'мақсад' аст.")
    elif "present simple" in text:
        await message.answer("Present Simple барои одатҳо истифода мешавад.")
    else:
        await message.answer("Ин саволро ҳанӯз намедонам.")
