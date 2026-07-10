from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNEL_USERNAME, ADMIN_ID
from database import add_user
from keyboards import get_subscribe_keyboard, get_main_menu

async def check_user_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Функсия барои санҷиши обунаи корбар ба канал"""
    user_id = update.effective_user.id
    
    # Агар ID-и корбар ба ADMIN_ID-и сохти config.py баробар бошад, бе санҷиш гузаронад
    if str(user_id) == str(ADMIN_ID):
        return True
        
    try:
        # Санҷиши статус дар канал
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Хатогии санҷиши обуна: {e}")
    
    return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вақте корбар /start менависад"""
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    
    is_subscribed = await check_user_subscribed(update, context)
    
    if is_subscribed:
        await update.message.reply_text(
            f"👋 Хуш омадед, {user.first_name}!\n\n"
            f"📚 Шумо ба канали мо обуна ҳастед. Аз менюи зер истифода баред:",
            reply_markup=get_main_menu()
        )
    else:
        await update.message.reply_text(
            f"👋 Салом, {user.first_name}!\n\n"
            f"🎯 Барои истифода бурдани ин бот ва гирифтани дарсҳову тестҳо, "
            f"аввал бояд ба канали расмии мо обуна шавед.",
            reply_markup=get_subscribe_keyboard()
        )

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вақте корбар тугмаи 'Обуна шудам (Санҷиш)'-ро пахш мекунад"""
    query = update.callback_query
    await query.answer()
    
    is_subscribed = await check_user_subscribed(update, context)
    
    if is_subscribed:
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="🎉 Табрик! Обунаи шумо тасдиқ шуд. Хуш омадед ба боти мо!",
            reply_markup=get_main_menu()
        )
    else:
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="❌ Шумо ҳанӯз ба канал обуна нашудаед. Лутфан аввал ҳамроҳ шавед ва бори дигар тугмаро пахш кунед.",
            reply_markup=get_subscribe_keyboard()
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Идораи тугмаҳои менюи асосӣ"""
    text = update.message.text
    is_subscribed = await check_user_subscribed(update, context)
    
    if not is_subscribed:
        await update.message.reply_text(
            "🔒 Лутфан аввал ба канал обуна шавед!",
            reply_markup=get_subscribe_keyboard()
        )
        return

    if text == "📚 Дарсҳо":
        await update.message.reply_text("📖 Дарсҳои нав ба зудӣ дар ин ҷо ва ҳар рӯз автоматӣ ба Simple English фиристода мешаванд!")
    elif text == "📝 Тестҳо":
        await update.message.reply_text("📝 Тестҳои ҳаррӯза ба зудӣ сохта мешаванд!")
    elif text == "📖 Китобҳои ройгон":
        await update.message.reply_text(f"📚 Китобҳои PDF-ро метавонед аз канали мо зеркашӣ кунед: {CHANNEL_USERNAME}")
    elif text == "ℹ️ Дар бораи мо":
        await update.message.reply_text(
            "👤 Муаллифи лоиҳа: Шералиев Абдураҳим\n"
            "📌 Мақсад: Омӯзиш ва дастгирии ҳамватанон дар роҳи омӯзиши забони англисӣ."
        )
