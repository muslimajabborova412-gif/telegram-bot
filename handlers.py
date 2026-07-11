from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Бот ба корбар чизе намегӯяд, ё метавонед як паёми оддӣ диҳед
    await message.answer("Бот фаъол аст ва ба канал постҳоро интиқол медиҳад.")
