import os
import random
from telebot import types
from gtts import gTTS # Ин китобхона барои сохтани овоз

# ... (қисми болоии код боқӣ мемонад) ...

def send_word_with_audio(chat_id, item):
    # 1. Фиристодани матн
    msg = (f"🔤 **{item['word']}**\n"
           f"🇹🇯 Тарҷума: {item['translation']}\n"
           f"📖 Таъриф: {item['definition']}\n"
           f"📝 Мисол: {item['example']}")
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    
    # 2. Сохтани аудио бо gTTS
    tts = gTTS(text=item['word'], lang='en')
    tts.save("word.mp3")
    
    # 3. Фиристодани аудио ҳамчун Voice
    with open("word.mp3", "rb") as audio:
        bot.send_voice(chat_id, audio)
    
    # Тоза кардани файл
    os.remove("word.mp3")

# Дар қисми list_unit_ (ба ҷои паёми оддӣ инро истифода мебарем):
# Ба ҷои bot.send_message... барои ҳар як калима инро даъват мекунем:
# for item in db[unit_number]:
#     send_word_with_audio(chat_id, item)
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    # Бот дар як поток (thread) ва Flask дар асосӣ
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
