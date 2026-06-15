async def select_unit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unit_number = update.message.text
    book_name = context.user_data.get('book')
    
    # Фарз мекунем, ки файлҳо дар ҳамон папкаи бот ҳастанд
    file_name = "book1.txt" if "1" in book_name else "book2.txt"
    
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        # Ин ҷо мо юнит-ро меёбем (боварӣ ҳосил кунед, ки дар файл "Unit 2" навишта шудааст)
        unit_found = False
        for line in lines:
            if f"Unit {unit_number}" in line:
                # Маълумотро тақсим мекунем: Калима - Тарҷума - Мисол
                parts = line.split("-")
                if len(parts) >= 3:
                    word, trans, ex = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    
                    # Фиристодани маълумот
                    await update.message.reply_text(f"📖 {word} — {trans}\n💬 {ex}")
                    
                    # Сохтан ва фиристодани аудио
                    tts = gTTS(text=word, lang='en')
                    tts.save("audio.mp3")
                    await update.message.reply_audio(audio=open("audio.mp3", "rb"))
                    os.remove("audio.mp3")
                    
        await update.message.reply_text("Ҳамаи калимаҳои ин юнит ба охир расиданд! ✅")
        
    except Exception as e:
        await update.message.reply_text(f"Хатогӣ рух дод: {e}")
        
    return ConversationHandler.END
