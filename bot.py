import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ТОКЕНИ БОТИ ХУДРО АЗ BOTFATHER ДАР БАЙНИ СИТАТАҲО ГУЗОР
TOKEN = '8996159898:AAEFani_soW7FmDlf2Uvrga0ruJKWfN9r64'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Салом! Боти ту дар Render бомуваффақият кор карда истодааст! 🚀')

def main() -> None:
    # Сохтани бот бо китобхонаи python-telegram-bot v20+
    application = Application.builder().token(TOKEN).build()

    # Илова кардани фармони /start
    application.add_handler(CommandHandler("start", start))

    print("Бот ба кор даромад ва логҳо фаъоланд...")
    # Сар кардани бот
    application.run_polling()

if __name__ == '__main__':
    main()
