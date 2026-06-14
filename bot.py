import os
import telebot
from telebot import types
from gtts import gTTS
import threading
from flask import Flask

# API TOKEN аз Environment гирифта мешавад
bot = telebot.TeleBot(os.environ.get('API_TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(f"U{i}", callback_data=f"unit_{i}") for i in range(1, 31)]
    markup.add(*buttons)
    bot.reply_to(message, "Салом! Барои омӯзиш Юнит-ро интихоб кунед:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("unit_"))
def handle_unit(call):
    unit_num = call.data.split("_")[1]
    
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        bot.answer_callback_query(call.id, "Файл ёфт нашуд!")
        return
        
    full_text = f"📚 **Юнити {unit_num}**\n\n"
    audio_text = ""
    found = False
    
    for line in lines:
        if line.strip().startswith(f"{unit_num};"):
            found = True
            parts = line.strip().split(';')
            # Формат: Юнит;Калима;Тарҷума;Мисол
            if len(parts) >= 4:
                full_text += f"🔹 *{parts[1]}* — {parts[2]}\n📝 {parts[3]}\n\n"
                # Танҳо калима ва мисол, бе калимаҳои Word ва Example
                audio_text += f"{parts[1]}. {parts[3]}. "
    
    if found:
        bot.send_message(call.message.chat.id, full_text, parse_mode="Markdown")
        
        # Эҷоди аудио бо суръати оҳиста (slow=True)
        try:
            tts = gTTS(text=audio_text, lang='en', slow=True)
            tts.save("unit.mp3")
            with open("unit.mp3", "rb") as audio:
                bot.send_voice(call.message.chat.id, audio)
            os.remove("unit.mp3")
        except Exception:
            bot.send_message(call.message.chat.id, "Хатогӣ дар эҷоди аудио.")
    else:
        bot.answer_callback_query(call.id, "Калимаҳо ёфт нашуданд.")

# Барои он ки Render ботро фаъол нигоҳ дорад
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
