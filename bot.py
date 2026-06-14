import logging
import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Танзими логҳо барои дидани хатогиҳо дар Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функсия барои хондани калимаҳо аз файл
def load_words(file_path):
    words = []
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(';')
                if len(parts) == 4:
                    words.append({
                        'unit': parts[0], 'word': parts[1],
                        'translation': parts[2], 'example': parts[3]
                    })
    except Exception as e:
        logging.error(f"Хатогӣ ҳангоми хондани файл: {e}")
        return None
    return words

# Функсияи асосӣ барои фиристодани калима
async def get_word(update: Update, context: ContextTypes.DEFAULT_TYPE, file_name: str, book_name: str):
    words = load_words(file_name)
    if not words:
        await update.message.reply_text(f"Хатогӣ: Файли {file_name} ёфт нашуд ё холӣ аст.")
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
    # Гирифтани токен аз Environment Variables дар Render
    TOKEN = os.getenv('BOT_TOKEN')
    
    if not TOKEN:
        print("Хатогӣ: BOT_TOKEN дар Render танзим нашудааст!")
    else:
        # Сохтани бот
        application = ApplicationBuilder().token(TOKEN).build()
        
        # Илова кардани командаҳо
        application.add_handler(CommandHandler('book1', book1))
        application.add_handler(CommandHandler('book2', book2))
        
        print("Бот бомуваффақият оғоз шуд!")
        application.run_polling()
