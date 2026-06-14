import os
import sys
import random

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

# Базаи калимаҳо аз китоби 4000 Essential English Words
WORDS_DATABASE = [
    {"word": "Agree", "translation": "Рози шудан", "example": "I agree with your opinion."},
    {"word": "Arrive", "translation": "Омадан, расидан", "example": "The train will arrive at 5 PM."},
    {"word": "Attack", "translation": "Ҳуҷум кардан", "example": "The dog attacked the stranger."},
    {"word": "Bottom", "translation": "Таг, поён", "example": "The coins were at the bottom of the sea."},
    {"word": "Clever", "translation": "Боҳуш, зирак", "example": "The clever boy solved the puzzle."},
    {"word": "Cruel", "translation": "Бераҳм, золим", "example": "The cruel man shouted at the kitten."},
    {"word": "Hide", "translation": "Пинҳон шудан", "example": "The children like to hide in the closet."},
    {"word": "Hunt", "translation": "Шикор кардан", "example": "Cats like to hunt mice."},
    {"word": "Lot", "translation": "Хеле бисёр", "example": "There are a lot of apples on the tree."},
    {"word": "Middle", "translation": "Муҳит, байн, марказ", "example": "He stood in the middle of the room."}
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "Салом, хуш омадед! 👋🇬🇧\n\n"
        "Ин бот барои омӯхтани **4000 Essential English Words** сохта шудааст!\n"
        "👨‍💻 **Созанда (Developer):** Абдурраҳим\n\n"
        "Фармонҳои мавҷуда:\n"
        "📖 /word - Гирифтани калимаи тасодуфӣ бо тарҷума\n"
        "🎲 /quiz - Санҷиши дониш (Тест)"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

@bot.message_handler(commands=['word'])
def send_word(message):
    item = random.choice(WORDS_DATABASE)
    text = (
        f"🔤 **Калима:** {item['word']}\n"
        f"🇹🇯 **Тарҷума:** {item['translation']}\n"
        f"📝 **Мисол:** _{item['example']}_"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['quiz'])
def send_quiz(message):
    correct_item = random.choice(WORDS_DATABASE)
    question = f"Тарҷумаи дурусти калимаи '{correct_item['word']}' кадом аст?"
    
    wrong_options = [item['translation'] for item in WORDS_DATABASE if item['translation'] != correct_item['translation']]
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
