from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Ҷавоби дуруст барои тести имрӯза
CORRECT_ANSWER = "goes"

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Салом! Ман ёрдамчии Абдураҳим ҳастам. Ҷавоби тести имрӯзаро нависед (масалан: goes):")

@router.message(F.text)
async def check_answer(message: Message):
    if message.text.lower() == CORRECT_ANSWER:
        await message.answer("🎉 Офарин! Ҷавоби шумо дуруст аст!")
    else:
        await message.answer(f"❌ Нодуруст. Ҷавоби дуруст '{CORRECT_ANSWER}' буд. Боз кӯшиш кунед!")
