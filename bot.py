import os
import sys
import random
from telebot import types

# Насби автоматии китобхонаҳо дар Render
try:
    import telebot
    from flask import Flask
except ModuleNotFoundError:
    os.system(f'"{sys.executable}" -m pip install pyTelegramBotAPI Flask')
    import telebot
    from flask import Flask

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Рӯйхати пурраи 20 калимаи Unit 1 мустақим аз рӯи матни ту
UNIT1_WORDS = [
    {"word": "Agree", "translation": "Рози шудан", "example": "I agree with your opinion."},
    {"word": "Alcohol", "translation": "Алкогол (нӯшокии спиртӣ)", "example": "Alcohol is bad for health."},
    {"word": "Arrive", "translation": "Омадан, расидан", "example": "The train will arrive at 5 PM."},
    {"word": "August", "translation": "Август", "example": "August is the eighth month of the year."},
    {"word": "Boat", "translation": "Қаиқ, киштӣ", "example": "We rode a small boat on the lake."},
    {"word": "Breakfast", "translation": "Нонушта", "example": "I had a healthy breakfast this morning."},
    {"word": "Camera", "translation": "Камера, аксбардорак", "example": "He took a picture with his new camera."},
    {"word": "Capital", "translation": "Пойтахт", "example": "Dushanbe is the capital of Tajikistan."},
    {"word": "Catch", "translation": "Доштан, қапидан", "example": "Did you catch the ball?"},
    {"word": "Duck", "translation": "Мурғобӣ", "example": "The duck is swimming in the pond."},
    {"word": "Enjoy", "translation": "Ҳаловат бурдан, маъқул шудан", "example": "We enjoyed our time at the beach."},
    {"word": "Invite", "translation": "Даъват кардан", "example": "They invited me to the party."},
    {"word": "Love", "translation": "Дӯст доштан, ишқ", "example": "I love my family very much."},
    {"word": "Month", "translation": "Моҳ", "example": "January is the first month of the year."},
    {"word": "Travel", "translation": "Саёҳат кардан", "example": "I want to travel to Japan."},
    {"word": "Typical", "translation": "Одатӣ, маъмулӣ", "example": "It was a typical cold winter day."},
    {"word": "Visit", "translation": "Хабар гирифтан, дидан кардан", "example": "I will visit my grandparents tomorrow."},
    {"word": "Weather", "translation": "Обу ҳаво", "example": "The weather is very hot today."},
    {"word": "Week", "translation": "Ҳафта", "example": "There are seven days in a week."},
    {"word": "Wine", "translation": "Шароб (вино)", "example": "Wine is made from grapes."}
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_words = types.KeyboardButton("📖 Луғат (Unit 1 Пурра)")
    btn_quiz = types.KeyboardButton("🎲 Савол (Тест)")
    markup.add(btn_words, btn_quiz)

    welcome_msg = (
        "Салом, хуш омадед! 👋🇬🇧\n\n"
        "Ин бот маҳз аз рӯи китоби **4000 Essential English Words 1** сохта шудааст! 📚\n"
        "👨‍💻 **Созанда (Developer):** Абдурраҳим\n\n"
        "Яке аз тугмаҳои поёнро интихоб кунед 👇"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "📖 Луғат (Unit 1 Пурра)":
        # Нишон додани ҳамаи 20 калима бо мисолҳояш
        response = "📚 **4000 Essential English Words 1**\n"
        response += "✨ **Unit 1 (Ҳамаи 20 калима):**\n\n"
        
        for i, item in enumerate(UNIT1_WORDS, 1):
            response += f"{i}. 🔤 **{item['word']}** - 🇹🇯 {item['translation']}\n📝 _Мисол:_ {item['example']}\n\n"
            
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
        
    elif message.text == "🎲 Савол (Тест)":
        # Тест аз байни ҳамаи 20 калима
        correct_item = random.choice(UNIT1_WORDS)
        question = f"Тарҷумаи дурусти калимаи '{correct_item['word']}' кадом аст?"
        
        wrong_options = [item['translation'] for item in UNIT1_WORDS if item['translation'] != correct_item['translation']]
        options = random.sample(wrong_options, 3)
        options.append(correct_item['translation'])
        random.shuffle(options)
        
        correct_index = options.index(correct_item['translation'])
        
        bot.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=options,
            type='quiz',
            correct_option_id=correct_index,
            is_anonymous=False
        )

# Веб-сервер барои Render
app = Flask(__name__)
@app.route('/')
def index(): return "Бот фаъол аст!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.polling(none_stop=True)
