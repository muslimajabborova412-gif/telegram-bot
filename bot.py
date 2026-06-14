import os
import threading
import telebot
from flask import Flask
from gtts import gTTS

# 1. Токенро аз Environment Variable мегирем (ин бехатар аст)
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# 2. Функсияи аудио
def send_word_with_audio(chat_id, item):
    msg = (f"🔤 **{item['word']}**\n"
           f"🇹🇯 Тарҷума: {item['translation']}\n"
           f"📖 Таъриф: {item['definition']}\n"
           f"📝 Мисол: {item['example']}")
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    
    tts = gTTS(text=item['word'], lang='en')
    tts.save("word.mp3")
    
    with open("word.mp3", "rb") as audio:
        bot.send_voice(chat_id, audio)
    os.remove("word.mp3")

# 3. Сервери Flask барои Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
