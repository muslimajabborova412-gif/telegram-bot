import os
from telegram.ext import ApplicationBuilder

# Ин сатр токенро аз Environment Variables-и Render мегирад
TOKEN = os.environ.get("BOT_TOKEN")

if __name__ == '__main__':
    if not TOKEN:
        print("Хатогӣ: BOT_TOKEN дар танзимот ёфт нашуд!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        # Дар ин ҷо handler-ҳои худро илова кунед
        application.run_polling()
