import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from gtts import gTTS

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)
app_bot = ApplicationBuilder().token(TOKEN).build()

# Функсия барои хондани калимаҳо
def get_unit_words(book_file, unit_num):
    words = []
    if not os.path.exists(book_file): return []
    with open(book_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) >= 4 and parts[0].strip() == str(unit_num):
                words.append(parts)
    return words

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    await update.message.reply_text("👋 Хуш омадед! Китобро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update, context):
    query = update.callback_query
    await query.answer()
    if query.data in ['book1', 'book2']:
        context.user_data['book'] = f"{query.data}.txt"
        keyboard = [[InlineKeyboardButton(f"Unit {i}", callback_data=f"unit_{i}")] for i in range(1, 31)]
        await query.edit_message_text(f"📖 Шумо {query.data}-ро интихоб кардед. Юнитро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith('unit_'):
        unit_num = query.data.split('_')[1]
        book_file = context.user_data.get('book')
        words = get_unit_words(book_file, unit_num)
        if not words:
            await query.edit_message_text("❌ Калима ёфт нашуд.")
            return
        await query.edit_message_text(f"✅ Юнити {unit_num} оғоз шуд...")
        for w in words:
            # ИН ҶО ПАРЧАМИ ТОҶИКИСТОН 🇹🇯
            word_text = f"🔤 **{w[1]}**\n🇹🇯 {w[2]}\n📝 {w[3]}"
            await context.bot.send_message(chat_id=query.message.chat_id, text=word_text, parse_mode='Markdown')
            tts = gTTS(text=f"{w[1]}. {w[3]}", lang='en')
            tts.save("speech.mp3")
            await context.bot.send_audio(chat_id=query.message.chat_id, audio=open("speech.mp3", "rb"))

app_bot.add_handler(CommandHandler('start', start))
app_bot.add_handler(CallbackQueryHandler(button))

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot.bot)
    app_bot.update_queue.put(update)
    return "ok"

if __name__ == '__main__':
    # URL-и худро дар Render дар ин ҷо навис (ҳамон суроғае, ки дар болои саҳифаи Render мебинед)
    bot = Bot(TOKEN)
    bot.set_webhook(url=f"https://YOUR-RENDER-APP-NAME.onrender.com/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
