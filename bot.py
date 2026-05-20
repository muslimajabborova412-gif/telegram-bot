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
        status_msg = bot.reply_to(message, "Дар ҳоли коркард ва табдили мусиқӣ... Лутфан сабр кунед. ⏳🎧")
        
        try:
            # Истифодаи сервери кушодаи дуюми содда барои гирифтани ссылкаи MP3
            api_url = f"https://api.v02.api-host.info/ytmp3?url={url}"
            response = requests.get(api_url, timeout=30).json()
            
            if response.get("status") == "success" or "download_url" in response:
                audio_url = response.get("download_url") or response.get("url")
                title = response.get("title", "Music")
                
                # Фиристодани мусиқӣ мустақиман тавассути ссылка ба Telegram
                bot.send_audio(message.chat.id, audio_url, caption=f"🎵 **{title}**\n\nТайёр шуд! 😉")
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                # Агар сервери аввал хато диҳад, бо усули дуюм кӯшиш мекунад
                api_url_2 = f"https://api.boxapi.xyz/youtube/v1/audio?url={url}"
                res2 = requests.get(api_url_2, timeout=30).json()
                audio_url = res2.get("url")
                if audio_url:
                    bot.send_audio(message.chat.id, audio_url, caption="Мусиқии шумо тайёр шуд! 🎵")
                    bot.delete_message(message.chat.id, status_msg.message_id)
                else:
                    bot.edit_message_text("Мутаассифона, серверҳо дар айни замон банд мебошанд. Лутфан дертар кӯшиш кунед. 🔄", message.chat.id, status_msg.message_id)
                    
        except Exception as e:
            bot.edit_message_text(f"Хатогии техникӣ: Сервер ҷавоб надод. Лутфан дубора кӯшиш кунед.", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "Лутфан ссылкаи дурусти YouTube-ро фиристед! ❌")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
