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
    {'word': 'Arrive', 'translation': 'Расидан', 'definition': 'To get somewhere', 'example': 'They arrived at school at 7 a.m.'},
    {'word': 'August', 'translation': 'Август', 'definition': 'The eighth month of the year', 'example': 'Is your birthday in August?'},
    {'word': 'Boat', 'translation': 'Қаиқ', 'definition': 'A vehicle that moves across water', 'example': 'There is a small boat on the lake.'},
    {'word': 'Breakfast', 'translation': 'Нонушта', 'definition': 'The morning meal', 'example': 'I ate eggs for breakfast.'},
    {'word': 'Camera', 'translation': 'Камера', 'definition': 'Equipment that takes pictures', 'example': 'I brought my camera on my vacation.'},
    {'word': 'Capital', 'translation': 'Пойтахт', 'definition': 'City where a country’s government is based', 'example': 'The capital of the USA is Washington, D.C.'},
    {'word': 'Catch', 'translation': 'Қапидан', 'definition': 'To grab or get something', 'example': 'Did you catch the ball?'},
    {'word': 'Duck', 'translation': 'Мурғобӣ', 'definition': 'A small water bird', 'example': 'People feed ducks at the lake.'}
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салом! Хуш омадед. Барои омӯзиш аз менюи поён тугмаи /unit1-ро пахш кунед.")

@bot.message_handler(commands=['unit1'])
def send_unit1(message):
    # 1. Навиштани матн
    full_text = "📚 **Калимаҳои Юнити 1:**\n\n"
    audio_text = ""
    for item in words_db:
        full_text += f"🔹 *{item['word']}* — {item['translation']}\n   📖 {item['definition']}\n   📝 {item['example']}\n\n"
        audio_text += f"{item['word']}. "

    bot.send_message(message.chat.id, full_text, parse_mode="Markdown")
    
    # 2. Аудиои ягона
    tts = gTTS(text=audio_text, lang='en')
    tts.save("unit1.mp3")
    with open("unit1.mp3", "rb") as audio:
        bot.send_voice(message.chat.id, audio, caption="🎧 Инҳо калимаҳои Юнити 1 мебошанд.")
    os.remove("unit1.mp3")

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is active!"

def run_bot():
    bot.infinity_polling(none_stop=True)

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
