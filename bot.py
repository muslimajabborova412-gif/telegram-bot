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
        status_msg = bot.reply_to(message, "Мусиқӣ дарёфт шуд. Дар ҳоли боркунӣ аз сервер... ⏳🎧")
        
        # Танзимоти Cobalt API махсус барои форматҳои аудиоӣ
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "filenamePattern": "classic",
            "downloadMode": "audio",  # Боркунии мустақим танҳо ба шакли аудио
            "audioFormat": "mp3"
        }
        
        try:
            # Истифодаи сервери устувори Cobalt API
            api_url = "https://api.cobalt.tools/api/json"
            response = requests.post(api_url, json=payload, headers=headers, timeout=20)
            result = response.json()
            
            # Агар сомона ссылкаи мустақимро баргардонад
            if result.get("status") == "stream" or result.get("status") == "picker":
                audio_url = result.get("url")
                
                # Агар видео якчанд формат дошта бошад
                if not audio_url and result.get("picker"):
                    audio_url = result["picker"][0].get("url")
                    
                if audio_url:
                    # Бор кардани суруд ва фиристодан ба корбар
                    file_path = "/tmp/music.mp3"
                    audio_data = requests.get(audio_url, stream=True)
                    
                    with open(file_path, 'wb') as f:
                        for chunk in audio_data.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                                
                    with open(file_path, 'rb') as audio_file:
                        bot.send_audio(message.chat.id, audio_file, caption="Мусиқии шумо бомуваффақият тайёр шуд! 😉🎵")
                        
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        
                    bot.delete_message(message.chat.id, status_msg.message_id)
                else:
                    bot.edit_message_text("Хатогӣ: Ссылкаи аудиоӣ ёфт нашуд. ❌", message.chat.id, status_msg.message_id)
            elif result.get("status") == "error":
                bot.edit_message_text(f"Хатогии API: {result.get('text')}", message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("Сервер банд аст, лутфан дубора кӯшиш кунед. 🔄", message.chat.id, status_msg.message_id)
                
        except Exception as e:
            bot.edit_message_text(f"Хатогии техникӣ: {e}\nЛутфан дубора кӯшиш кунед.", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "Лутфан ссылкаи дурусти YouTube-ро фиристед! ❌")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
