import os
import threading
import telebot
from flask import Flask
from gtts import gTTS
from telebot import types

# Токен аз Render гирифта мешавад
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Базаи калимаҳои Юнити 1
words_db = [
    {'word': 'Agree', 'translation': 'Рози шудан', 'definition': 'To have the same opinion as another person', 'example': 'The students agree they have too much homework.'},
    {'word': 'Alcohol', 'translation': 'Алкогол', 'definition': 'A drink that can make people drunk', 'example': 'A person should not drive a car after drinking alcohol.'},
    {'word': 'Arrive', 'translation': 'Расидан', 'definition': 'To get somewhere', 'example': 'They arrived at school at 7 a.m.'},
    {'word': 'August', 'translation': 'Август', 'definition': 'The eighth month of the year', 'example': 'Is your birthday in August?'},
    {'word': 'Boat', 'translation': 'Қаиқ', 'definition': 'A vehicle that moves across water', 'example': 'There is a small boat on the lake.'},
    {'word': 'Breakfast', 'translation': 'Нонушта', 'definition': 'The morning meal', 'example': 'I ate eggs for breakfast.'},
    {'word': 'Camera', 'translation': 'Камера', 'definition': 'Equipment that takes pictures', 'example': 'I brought my camera on my vacation.'},
    {'word': 'Capital', 'translation': 'Пойтахт', 'definition': 'City where a country’s government is based', 'example': 'The capital of the USA is Washington, D.C.'},
    {'word': 'Catch', 'translation': 'Қапидан', 'definition': 'To grab or get something', 'example': 'Did you catch the ball?'},
    {'word': 'Duck', 'translation': 'Мурғобӣ', 'definition': 'A small water bird', 'example': 'People feed ducks at the lake.'},
    {'word': 'Enjoy', 'translation': 'Ҳаловат бурдан', 'definition': 'To like something', 'example': 'The woman enjoys riding her bicycle.'},
    {'word': 'Invite', 'translation': 'Даъват кардан', 'definition': 'To ask someone to come to an event', 'example': 'I will invite my friends to my party.'},
    {'word': 'Love', 'translation': 'Дӯст доштан', 'definition': 'To like something a lot', 'example': 'I love my family very much.'},
    {'word': 'Month', 'translation': 'Моҳ', 'definition': 'One of 12 periods of time in one year', 'example': 'January is the first month.'},
    {'word': 'Travel', 'translation': 'Саёҳат кардан', 'definition': 'To go to a faraway place', 'example': 'They will travel to Argentina.'},
    {'word': 'Typical', 'translation': 'Одатӣ', 'definition': 'Normal, usually happens', 'example': 'My typical breakfast is toast and eggs.'},
    {'word': 'Visit', 'translation': 'Хабар гирифтан', 'definition': 'To spend time in another place', 'example': 'She wants to visit her grandmother.'},
    {'word': 'Weather', 'translation': 'Обу ҳаво', 'definition': 'The state of the outdoors', 'example': 'Today\'s weather is rainy.'},
    {'word': 'Week', 'translation': 'Ҳафта', 'definition': 'A period of seven days', 'example': 'What are you doing next week?'},
    {'word': 'Wine', 'translation': 'Шароб', 'definition': 'An alcoholic drink from grapes', 'example': 'The store carried red wine.'}
]

def send_word(chat_id, index):
    item = words_db[index]
    msg = (f"🔤 **Калима:** {item['word']}\n"
           f"🇹🇯 **Тарҷума:** {item['translation']}\n"
           f"📖 **Таъриф:** {item['definition']}\n"
           f"📝 **Мисол:** {item['example']}")
    
    markup = types.InlineKeyboardMarkup()
    if index + 1 < len(words_db):
        btn = types.InlineKeyboardButton("➡️ Калимаи нав", callback_data=f"next_{index + 1}")
        markup.add(btn)
    
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)
    
    # Овоз бояд тамоми маълумотро хонад
    full_audio_text = f"Word: {item['word']}. Translation: {item['translation']}. Definition: {item['definition']}. Example: {item['example']}"
    tts = gTTS(text=full_audio_text, lang='en')
    tts.save("word.mp3")
    
    with open("word.mp3", "rb") as audio:
        bot.send_voice(chat_id, audio)
    os.remove("word.mp3")

@bot.callback_query_handler(func=lambda call: call.data.startswith("next_"))
def next_word(call):
    index = int(call.data.split("_")[1])
    send_word(call.message.chat.id, index)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салом! Барои оғози Юнити 1 нависед: /unit1")

@bot.message_handler(commands=['unit1'])
def start_unit1(message):
    send_word(message.chat.id, 0)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_bot(): bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
