from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from database import init_db
from handlers import start_command, button_callback_handler, text_handler
from scheduler import start_scheduler

def main():
    # 1. Сар кардани Базаи маълумот
    init_db()
    
    # 2. Сохтани лоиҳаи Бот бо JobQueue
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # 3. Пайваст кардани командаҳо ва тугмаҳо
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_callback_handler, pattern="^check_subscription$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    # 4. Фаъол кардани автопостинг
    start_scheduler(application)
    
    # 5. Ба кор андохтани бот
    print("Бот бомуваффақият фаъол шуд...")
    application.run_polling()

if __name__ == "__main__":
    main()
