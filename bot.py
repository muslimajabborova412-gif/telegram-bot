# 1. Аввал импортҳо
import os
import asyncio
# ... (дигар импортҳо)

# 2. Баъд функсияҳоро муайян кунед
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("4000 Essential English Words 1", callback_data='book1')],
        [InlineKeyboardButton("4000 Essential English Words 2", callback_data='book2')]
    ]
    await update.message.reply_text("Китобро интихоб кунед:", reply_markup=InlineKeyboardMarkup(keyboard))

# ... (дигар функсияҳои callback-и шумо)

# 3. Ва ТАНҲО БАЪД АЗ ОН, Handler-ҳоро илова кунед
app_bot = ApplicationBuilder().token(TOKEN).build()
app_bot.add_handler(CommandHandler('start', start))
app_bot.add_handler(CallbackQueryHandler(book_callback, pattern=r'^book[12]$'))
# ... ва ҳоказо
