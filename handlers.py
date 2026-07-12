from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Ин "базаи дониш"-и шумо аст. Ҳар рӯз метавонед инро нав кунед.
TEST_DATABASE = {
    "goes": {
        "explanation": "Дар замони Present Simple барои шахси 3-юм (he, she, it) ба феъл -es илова мешавад. 'She goes' дуруст аст.",
        "topic": "Present Simple"
    },
    "playing": {
        "explanation": "Барои замони Continuous (ҳозира) мо 'be + verb-ing' истифода мебарем. 'He is playing' дуруст аст.",
        "topic": "Present Continuous"
    }
}

@router.message(F.text)
async def check_answer(message: Message):
    user_answer = message.text.lower()
    
    # Санҷиш, ки оё ҷавоб дар базаи мо ҳаст
    if user_answer in TEST_DATABASE:
        data = TEST_DATABASE[user_answer]
        await message.answer(f"✅ Офарин! Ҷавоби шумо дуруст аст дар мавзӯи {data['topic']}.")
    else:
        # Агар хато кунад, бот маълумоти пурра медиҳад
        await message.answer("❌ Ҷавоби шумо нодуруст буд.\n\n"
                             "📖 **Маълумоти иловагӣ барои шумо:**\n"
                             "Мо бояд дар хотир дорем, ки ин қоидаро бояд такрор кунем. "
                             "Лутфан, дарсро дубора хонед ва кӯшиш кунед!")
