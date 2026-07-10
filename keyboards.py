from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import CHANNEL_USERNAME

def get_subscribe_keyboard():
    """Тугмаҳо барои маҷбур кардани корбар ба обуна шудан"""
    keyboard = [
        [InlineKeyboardButton("📢 Ба канал ҳамроҳ шувед", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("✅ Обуна шудам (Санҷиш)", callback_data="check_subscription")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu():
    """Менюи асосии бот баъд аз обуна шудан"""
    keyboard = [
        [KeyboardButton("📚 Дарсҳо"), KeyboardButton("📝 Тестҳо")],
        [KeyboardButton("📖 Китобҳои ройгон"), KeyboardButton("ℹ️ Дар бораи мо")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
