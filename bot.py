import os
from flask import Flask, request
import telebot
import yt_dlp

# Токен ва Ссылкаро аз Render автоматӣ мегирад ё метавони худат дастӣ нависӣ
TOKEN = os.environ.get('BOT_TOKEN', '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ')
WEBHOOK_URL = 'https://telegram-bot-quiz-3cqc.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook_setup():
    bot.remove_webhook()
    status = bot.set_webhook(url=WEBHOOK_URL + '/' + TOKEN)
    return f"Webhook status: {status} 🚀"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салом! Ссылкаи YouTube-ро ба ман фиристед, ман онро ба MP3 табдил медиҳам! 🎧😎")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = bot.reply_to(message, "Дар ҳоли коркарди мусиқӣ... Каме сабр кунед. ⏳🎧")
        
        # Боркунӣ танҳо ба шакли аудио
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'noplaylist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            # Фиристодани файл ба корбар
            with open(filename, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file, caption="Мусиқии шумо тайёр шуд! 😉")
            
            # Тоза кардани файл аз хотираи сервер пас аз фиристодан
            if os.path.exists(filename):
                os.remove(filename)
                
            bot.delete_message(message.chat.id, status_msg.message_id)
            
        except Exception as e:
            bot.reply_to(message, f"Хатогии техникӣ рӯй дод: {e}")
    else:
        bot.reply_to(message, "Лутфан ссылкаи дурусти YouTube-ро фиристед! ❌")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
