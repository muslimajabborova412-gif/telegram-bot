from telegram.ext import ApplicationBuilder, CommandHandler

# Функция барои хондани файл
def read_book(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Файл ёфт нашуд."

# Фармон барои book1
async def send_book1(update, context):
    text = read_book('book1.txt')
    await update.message.reply_text(text)

# Фармон барои book2
async def send_book2(update, context):
    text = read_book('book2.txt')
    await update.message.reply_text(text)

if __name__ == '__main__':
    application = ApplicationBuilder().token("ТОКЕНИ_ШУМО").build()
    
    application.add_handler(CommandHandler("book1", send_book1))
    application.add_handler(CommandHandler("book2", send_book2))
    
    application.run_polling()
