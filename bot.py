import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import random

# Танзими логҳо
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функсия барои хондани калимаҳо
def load_words(file_path):
    words = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) == 4:
                    words.append({
                        'unit': parts[0], 'word': parts[1],
                        'translation': parts[2], 'example': parts[3]
                    })
    except FileNotFoundError:
        return None
    return words

async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name: str, book_name: str):
    words = load_words(file_name)
    if not words:
        await update.message.reply_text(f"Хатогӣ: Файли {book_name} ёфт нашуд ё холӣ аст.")
        return
    
    word_obj = random.choice(words)
    response = (f"📚 **{book_name}**\n"
                f"📖 **Юнит:** {word_obj['unit']}\n"
                f"🔤 **Калима:** {word_obj['word']}\n"
                f"🇺🇿 **Тарҷума:** {word_obj['translation']}\n"
                f"📝 **Мисол:** {word_obj['example']}")
    await update.message.reply_text(response, parse_mode='Markdown')

# Командаҳо
async def book1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_word(update, context, 'book1.txt', 'Китоби 1 (4000 Words)')

async def book2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_word(update, context, 'book2.txt', 'Китоби 2 (4000 Words)')

if __name__ == '__main__':
    application = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()
    
    application.add_handler(CommandHandler('book1', book1))
    application.add_handler(CommandHandler('book2', book2))
    
    application.run_polling()
