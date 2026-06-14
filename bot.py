import os
import telebot
from flask import Flask
from gtts import gTTS
import threading

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))

@bot.message_handler(commands=[f'unit{i}' for i in range(1, 31)])
def handle_unit(message):
    unit_num = message.text.replace('/unit', '').strip() # Фосилаҳоро тоза мекунад
    
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        bot.reply_to(message, "Файли words.txt ёфт нашуд!")
        return
        
    full_text = f"📚 **Юнити {unit_num}**\n\n"
    audio_text = ""
    found = False
    
    for line in lines:
        line = line.strip() # Ҳамаи фосилаҳои иловагиро аз ду тараф тоза мекунад
        if not line: continue
        
        parts = line.split(';')
        
        # Ин ҷо мо рақами Юнитро бо рақами дар сатр буда муқоиса мекунем
        if len(parts) >= 4 and parts[0].strip() == unit_num:
            found = True
            full_text += f"🔹 *{parts[1]}* — {parts[2]}\n📝 {parts[3]}\n\n"
            audio_text += f"{parts[1]}. "
    
    if not found:
        bot.reply_to(message, f"Калимаҳои Юнити {unit_num} ёфт нашуданд.")
    else:
        bot.send_message(message.chat.id, full_text, parse_mode="Markdown")
        
        # Эҷоди аудио
        tts = gTTS(text=audio_text, lang='en')
        tts.save("unit.mp3")
        with open("unit.mp3", "rb") as audio:
            bot.send_voice(message.chat.id, audio)
        os.remove("unit.mp3")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Салом! Барои омӯзиш аз /unit1 то /unit30 истифода баред.")

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
