import os
import telebot
import yt_dlp

# Render худаш токени боти кӯҳнаатро автоматӣ ба ин ҷо мегузорад
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салом! Ссылкаи YouTube-ро ба ман фиристед, ман онро ба MP3 табдил медиҳам! 🎧😎")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "Дар ҳоли коркарди мусиқӣ... Каме сабр кунед. ⏳🎧")
        
        # Танзимоти файл барои Render (сабт дар папкаи вақтии /tmp)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/music.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            audio_path = '/tmp/music.mp3'
            with open(audio_path, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file, caption="Мусиқии шумо тайёр шуд! Ташаккур барои истифода. 😉")
            
            os.remove(audio_path)
        except Exception as e:
            bot.reply_to(message, f"Хатогии техникӣ рӯй дод: {e}")
    else:
        bot.reply_to(message, "Лутфан ссылкаи дурусти YouTube-ро фиристед! ❌")

# Барои фаъол нигоҳ доштани Web Service дар Render (Flask)
from flask import Flask
app = Flask(name)
@app.route('/')
def index(): return "Бот фаъол аст!"

if name == "main":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.polling(none_stop=True)
