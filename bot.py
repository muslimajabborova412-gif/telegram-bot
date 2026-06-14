import os
import threading
import telebot
from flask import Flask
from gtts import gTTS

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Базаи калимаҳо (Юнити 1)
words_db = [
    {'word': 'Agree', 'translation': 'Рози шудан', 'definition': 'To have the same opinion as another person', 'example': 'The students agree they have too much homework.'},
    {'word': 'Alcohol', 'translation': 'Алкогол', 'definition': 'A drink that can make people drunk', 'example': 'A person should not drive a car after drinking alcohol.'},
    # ... (дигар 18 калимаи дигарро илова кун)
]

@bot.message_handler(commands=['unit1'])
def send_unit1(message):
    # 1. Тайёр кардани матни пурра барои корбар
    full_text = "📚 **Калимаҳои Юнити 1:**\n\n"
    audio_text = ""
    
    for item in words_db:
        full_text += (f"🔤 {item['word']} - {item['translation']}\n"
                      f"📖 {item['definition']}\n"
                      f"📝 {item['example']}\n\n")
        # Танҳо калимаҳоро барои аудио ҷамъ мекунем
        audio_text += f"{item['word']}. "

    # 2. Фиристодани матн
    bot.send_message(message.chat.id, full_text, parse_mode="Markdown")
    
    # 3. Сохтани як аудиои калон барои ҳамаи калимаҳо
    tts = gTTS(text=audio_text, lang='en')
    tts.save("unit1.mp3")
    
    # 4. Фиристодани аудио
    with open("unit1.mp3", "rb") as audio:
        bot.send_voice(message.chat.id, audio, caption="🎧 Гӯш кунед ва такрор кунед!")
    
    os.remove("unit1.mp3")

# (Қисми Flask ва run_bot мисли пештара боқӣ мемонад)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is active!"

def run_bot(): bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
