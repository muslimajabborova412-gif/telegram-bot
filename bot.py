import os
import requests
from flask import Flask, request
import telebot

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
        status_msg = bot.reply_to(message, "Дар ҳоли дарёфт ва коркарди мусиқӣ бо сервери алтернативӣ... ⏳🎧")
        
        # Эълони ID-и видео аз ссылка
        video_id = ""
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        elif "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
            
        if not video_id:
            bot.edit_message_text("Ссылкаи YouTube нодуруст аст! ❌", message.chat.id, status_msg.message_id)
            return

        try:
            # Истифодаи сервери кушодаи Invidious барои гирифтани аудио-ссылкаи мустақим
            api_url = f"https://invidious.io.lol/api/v1/videos/{video_id}"
            response = requests.get(api_url, timeout=15).json()
            
            # Ёфтани беҳтарин файл бо формати аудио
            audio_url = None
            for fmt in response.get('adaptiveFormats', []):
                if fmt.get('type', '').startswith('audio/'):
                    audio_url = fmt.get('url')
                    break
            
            if not audio_url:
                # Агар дар сервери аввал наёфт, сервери дуюмро тафтиш мекунад
                api_url = f"https://vid.puffyan.us/api/v1/videos/{video_id}"
                response = requests.get(api_url, timeout=15).json()
                for fmt in response.get('adaptiveFormats', []):
                    if fmt.get('type', '').startswith('audio/'):
                        audio_url = fmt.get('url')
                        break

            if audio_url:
                # Бор кардани файл ба хотираи сервер ва фиристодан ба Telegram
                file_path = f"/tmp/{video_id}.mp3"
                audio_data = requests.get(audio_url, stream=True)
                
                with open(file_path, 'wb') as f:
                    for chunk in audio_data.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                
                with open(file_path, 'rb') as audio_file:
                    title = response.get('title', 'Music')
                    bot.send_audio(message.chat.id, audio_file, caption=f"🎵 **{title}**\n\nТайёр шуд! 😉", parse_mode="Markdown")
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("Мутаассифона, аудио барои ин видео пайдо нашуд. ❌", message.chat.id, status_msg.message_id)
                
        except Exception as e:
            bot.edit_message_text(f"Хатогии техникӣ дар сервер: {e}\nЛутфан дубора кӯшиш кунед.", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "Лутфан ссылкаи дурусти YouTube-ро фиристед! ❌")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
