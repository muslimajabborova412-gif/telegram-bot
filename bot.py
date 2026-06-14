import os
import threading
import telebot
from flask import Flask
from gtts import gTTS
from telebot import types
import time

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Базаи калимаҳо (бо тарҷума ва таърифи англисӣ)
words_db = [
    {'word': 'Agree', 'translation': 'Рози шудан', 'definition': 'To have the same opinion as another person', 'example': 'The students agree they have too much homework.'},
    {'word': 'Alcohol', 'translation': 'Алкогол', 'definition': 'A drink that can make people drunk', 'example': 'A person should not drive a car after drinking alcohol.'}
]

# Функсияи аудио (танҳо англисӣ)
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
    
    # Танҳо калима ва таърифро мехонад
    audio_text = f"{item['word']}. {item['definition']}"
    tts = gTTS(text=audio_text, lang='en')
    tts.save("word.mp3")
    
    with open("word.mp3", "rb") as audio:
        bot.send_voice(chat_id, audio)
    os.remove("word.mp3")

@bot.callback_query_handler(func=lambda call: call.data.startswith("next_"))
def next_word(call):
    index = int(call.data.split("_")[1])
    if index < len(words_db):
        send_word(call.message.chat.id, index)

@bot.message_handler(commands=['unit1'])
def start_unit1(message):
    send_word(message.chat.id, 0)

# Қисми муҳим: Сервер барои Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(5) # Агар хато шавад, 5 сония интизор мешавем

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
