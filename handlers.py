from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Ин функсия ҷавобҳои корбарро месанҷад
@router.message(F.text)
async def check_answer(message: Message):
    # Масалан, агар корбар калимаи "apple" нависад
    if message.text.lower() == "apple":
        await message.answer("✅ Офарин! Ҷавоби дуруст.")
    else:
        await message.answer("❌ Мутаассифона, ҷавоб нодуруст аст. Боз кӯшиш кунед!")
