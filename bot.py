import os
from flask import Flask, request
import telebot
import yt_dlp

TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'
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
        status_msg = bot.reply_to(message, "Дар ҳоли коркарди мусиқӣ ва давр задани блокҳои YouTube... Лутфан 1-2 дақиқа сабр кунед. ⏳🎧")
        
        # Танзимоти махсус барои гузаштани Блок ва Эрори "Sign in to confirm you're not a bot"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/%(id)s.%(ext)s',
            'noplaylist': True,
            # Ин қисм ботро ҳамчун корбари оддии Android нишон медиҳад:
            'impersonate': 'chrome', 
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['dash', 'hls']
                }
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file, caption="Мусиқии шумо бомуваффақият тайёр шуд! 😉🎵")
            
            if os.path.exists(filename):
                os.remove(filename)
                
            bot.delete_message(message.chat.id, status_msg.message_id)
            
        except Exception as e:
            # Агар боз хатогӣ диҳад, кӯшиш мекунад бо усули сабуктар бор кунад
            bot.edit_message_text(f"Хатогии аввалия: {e}\n\nҚадами дуюм: Кӯшиши боркунӣ бо сервери алтернативӣ... 🔄", message.chat.id, status_msg.message_id)
            try:
                ydl_opts['format'] = 'waorst_audio/worst'
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                with open(filename, 'rb') as audio_file:
                    bot.send_audio(message.chat.id, audio_file, caption="Мусиқии шумо тайёр шуд! 😉")
                if os.path.exists(filename): os.remove(filename)
                bot.delete_message(message.chat.id, status_msg.message_id)
            except Exception as e2:
                bot.reply_to(message, f"Мутаассифона, YouTube ин видеоро пурра блок кард. Хатогӣ: {e2}")
    else:
        bot.reply_to(message, "Лутфан ссылкаи дурусти YouTube-ро фиристед! ❌")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
