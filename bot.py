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
