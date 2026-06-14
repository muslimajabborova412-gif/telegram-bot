def send_word(chat_id, index):
    item = words_db[index]
    msg = (f"🔤 **Калима:** {item['word']}\n"
           f"🇹🇯 **Тарҷума:** {item['translation']}\n"
           f"📖 **Таъриф:** {item['definition']}\n"
           f"📝 **Мисол:** {item['example']}")
    
    markup = types.InlineKeyboardMarkup()
    if index + 1 < len(words_db):
        btn = types.InlineKeyboardButton("➡️ Калимаи нав", callback_data=f"next_{index + 1}")
        markup.add(btn)
    
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)
    
    # ТАНҲО КАЛИМА ВА ТАЪРИФИ АНГЛИСИРО МЕХОНАД (ки хушсадо бошад)
    audio_text = f"{item['word']}. {item['definition']}"
    tts = gTTS(text=audio_text, lang='en')
    tts.save("word.mp3")
    
    with open("word.mp3", "rb") as audio:
        bot.send_voice(chat_id, audio)
    os.remove("word.mp3")
