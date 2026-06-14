import os
import threading
import telebot
from flask import Flask
from gtts import gTTS

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Базаи калимаҳои Юнити 1
words_db = [
    {'word': 'Agree', 'translation': 'Рози шудан', 'definition': 'To have the same opinion as another person', 'example': 'The students agree they have too much homework.'},
    {'word': 'Alcohol', 'translation': 'Алкогол', 'definition': 'A drink that can make people drunk', 'example': 'A person should not drive a car after drinking alcohol.'},
    {'word': 'Arrive', 'translation': 'Омадан', 'definition': 'To get somewhere', 'example': 'They arrived at school at 7 a.m.'},
    {'word': 'August', 'translation': 'Август', 'definition': 'The eighth month of the year', 'example': 'Is your birthday in August?'},
    {'word': 'Boat', 'translation': 'Қаиқ', 'definition': 'A vehicle that moves across water', 'example': 'There is a small boat on the lake.'},
    {'word': 'Breakfast', 'translation': 'Нонушта', 'definition': 'The morning meal', 'example': 'I ate eggs for breakfast.'},
    {'word': 'Camera', 'translation': 'Камера', 'definition': 'Equipment that takes pictures', 'example': 'I brought my camera on my vacation.'},
    {'word': 'Capital', 'translation': 'Пойтахт', 'definition': 'A city where a country’s government is based', 'example': 'The capital of the US is Washington, D.C.'},
    {'word': 'Catch', 'translation': 'Қапидан', 'definition': 'To grab or get something', 'example': 'Did you catch the ball?'},
    {'word': 'Duck', 'translation': 'Мурғобӣ', 'definition': 'A small water bird', 'example': 'People feed ducks at the lake.'},
    {'word': 'Enjoy', 'translation': 'Ҳаловат бурдан', 'definition': 'To like something', 'example': 'The woman enjoys riding her bicycle.'},
    {'word': 'Invite', 'translation': 'Даъват кардан', 'definition': 'To ask someone to come to an event', 'example': 'I will invite my friends to my party.'},
    {'word': 'Love', 'translation': 'Дӯст доштан', 'definition': 'To like something a lot', 'example': 'I love my family very much.'},
    {'word': 'Month', 'translation': 'Моҳ', 'definition': 'One of 12 periods in a year', 'example': 'January is the first month.'},
    {'word': 'Travel', 'translation': 'Саёҳат кардан', 'definition': 'To go to a faraway place', 'example': 'They will travel to Argentina.'},
    {'word': 'Typical', 'translation': 'Одатӣ', 'definition': 'Normal, usually happens', 'example': 'My typical breakfast is toast and eggs.'},
    {'word': 'Visit', 'translation': 'Хабар гирифтан', 'definition': 'To spend time in another place', 'example': 'She wants to visit her grandmother.'},
    {'word': 'Weather', 'translation': 'Обу ҳаво', 'definition': 'The state of the outdoors', 'example': 'Today\'s weather is rainy.'},
    {'word': 'Week', 'translation': 'Ҳафта', 'definition': 'A period of seven days', 'example': 'What are you doing next week?'},
    {'word': 'Wine', 'translation': 'Шароб', 'definition': 'An alcoholic drink from grapes', 'example': 'The store carried red wine.'}
]

def send_word_with_audio(chat_id, item):
    msg = (f"🔤 **{item['word']}**\n🇹🇯 Тарҷума: {item['translation']}\n"
           f"📖 Таъриф: {item['definition']}\n📝 Мисол: {item['example']}")
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    tts = gTTS(text=item['word'], lang='en')
    tts.save("word.mp3")
    with open("word.mp3", "rb") as audio:
        bot.send_voice(chat_id, audio)
    os.remove("word.mp3")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салом! Барои Юнити 1 нависед: /unit1")

@bot.message_handler(commands=['unit1'])
def send_unit1(message):
    for item in words_db:
        send_word_with_audio(message.chat.id, item)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_bot(): bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
