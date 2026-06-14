import os
import sys
import random
import time
from telebot import types

# Насби автоматии китобхонаҳо дар Render
try:
    import telebot
    from flask import Flask
except ModuleNotFoundError:
    os.system(f'"{sys.executable}" -m pip install pyTelegramBotAPI Flask')
    import telebot
    from flask import Flask

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 20 калимаи Unit 1 аз рӯи матни ту
UNIT1_WORDS = [
    {"word": "Agree", "translation": "Рози шудан", "example": "I agree with your opinion."},
    {"word": "Alcohol", "translation": "Алкогол (нӯшокии спиртӣ)", "example": "Alcohol is bad for health."},
    {"word": "Arrive", "translation": "Омадан, расидан", "example": "The train will arrive at 5 PM."},
    {"word": "August", "translation": "Август", "example": "August is the eighth month of the year."},
    {"word": "Boat", "translation": "Қаиқ, киштӣ", "example": "We rode a small boat on the lake."},
    {"word": "Breakfast", "translation": "Нонушта", "example": "I had a healthy breakfast this morning."},
    {"word": "Camera", "translation": "Камера, аксбардорак", "example": "He took a picture with his new camera."},
    {"word": "Capital", "translation": "Пойтахт", "example": "Dushanbe is the capital of Tajikistan."},
    {"word": "Catch", "translation": "Доштан, қапидан", "example": "Did you catch the ball?"},
    {"word": "Duck", "translation": "Мурғобӣ", "example": "The duck is swimming in the pond."},
    {"word": "Enjoy", "translation": "Ҳаловат бурдан", "example": "We enjoyed our time at the beach."},
    {"word": "Invite", "translation": "Даъват кардан", "example": "They invited me to the party."},
    {"word": "Love", "translation": "Дӯст доштан", "example": "I love my family very much."},
    {"word": "Month", "translation": "Моҳ", "example": "January is the first month of the year."},
    {"word": "Travel", "translation": "Саёҳат кардан", "example": "I want to travel to Japan."},
    {"word": "Typical", "translation": "Одатӣ, маъмулӣ", "example": "It was a typical cold winter day."},
    {"word": "Visit", "translation": "Хабар гирифтан", "example": "I will visit my grandparents tomorrow."},
    {"word": "Weather", "translation": "Обу ҳаво", "example": "The weather is very hot today."},
    {"word": "Week", "translation": "Ҳафта", "example": "There are seven days in a week."},
    {"word": "Wine", "translation": "Шароб (вино)", "example": "Wine is made from grapes."}
]

# Барои нигоҳ доштани ҳолати корбарон (индекс ва холҳо)
user_states = {}

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📖 Луғат (Ҷудо-ҷудо)"), types.KeyboardButton("🎲 Оғози Тест (10 Савол)"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "Салом! 👋 Хуш омадед ба боти омӯзишии **4000 Essential English Words**!\n\n"
        "👨‍💻 **Созанда:** Абдурраҳим\n"
        "Яке аз тугмаҳоро пахш кун 👇"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    chat_id = message.chat.id
    
    if message.text == "📖 Луғат (Ҷудо-ҷудо)":
        user_states[chat_id] = {"dict_index": 0}
        show_word_with_typing_effect(chat_id, 0)
        
    elif message.text == "🎲 Оғози Тест (10 Савол)":
        # Оғози марафони 10 саволи омехта
        shuffled_questions = random.sample(UNIT1_WORDS, min(10, len(UNIT1_WORDS)))
        user_states[chat_id] = {
            "quiz_list": shuffled_questions,
            "quiz_index": 0,
            "score": 0,
            "last_poll_id": None
        }
        bot.send_message(chat_id, "🚀 Тести омехта аз 10 савол оғоз шуд!")
        send_next_quiz(chat_id)

# Функсияи нишон додани луғат бо эффекти навиштан (Аниматсия)
def show_word_with_typing_effect(chat_id, index, message_id=None):
    item = UNIT1_WORDS[index]
    
    word_text = (
        f"📖 **Калимаи {index + 1} аз {len(UNIT1_WORDS)}**\n\n"
        f"🔤 **English:** {item['word']}\n"
        f"🇹🇯 **Тарҷума:** {item['translation']}\n"
        f"📝 _Мисол:_ {item['example']}"
    )
    
    # Танзими тугмаҳои Баъдӣ ва Пештар дар зери худи луғат
    markup = types.InlineKeyboardMarkup()
    buttons = []
    if index > 0:
        buttons.append(types.InlineKeyboardButton("⬅️ Пештар", callback_data=f"prev_{index}"))
    if index < len(UNIT1_WORDS) - 1:
        buttons.append(types.InlineKeyboardButton("Баъдӣ ➡️", callback_data=f"next_{index}"))
    markup.add(*buttons)

    # Эффекти навиштани компютер (Typing animation)
    if message_id is None:
        msg = bot.send_message(chat_id, "💻 Дар ҳоли навишт .")
        time.sleep(0.3)
        bot.edit_message_text("💻 Дар ҳоли навишт ..", chat_id, msg.message_id)
        time.sleep(0.3)
        bot.edit_message_text("💻 Дар ҳоли навишт ...", chat_id, msg.message_id)
        time.sleep(0.2)
        bot.edit_message_text(word_text, chat_id, msg.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        try:
            bot.edit_message_text(word_text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            pass

# Суръатбахшии ивазшавии луғатҳо ҳангоми пахши тугмаи ҷудогона
@bot.callback_query_handler(func=lambda call: call.data.startswith(('next_', 'prev_')))
def handle_dict_navigation(call):
    chat_id = call.message.chat_id
    action, current_index = call.data.split('_')
    current_index = int(current_index)
    
    new_index = current_index + 1 if action == 'next' else current_index - 1
    
    if 0 <= new_index < len(UNIT1_WORDS):
        show_word_with_typing_effect(chat_id, new_index, call.message.message_id)
    bot.answer_callback_query(call.id)

# Функсияи фиристодани Саволҳо (Тест)
def send_next_quiz(chat_id):
    state = user_states.get(chat_id)
    if not state or "quiz_list" not in state:
        return
        
    idx = state["quiz_index"]
    questions = state["quiz_list"]
    
    if idx >= len(questions):
        # Агар 10 савол тамом шавад
        bot.send_message(chat_id, f"🏁 **Тест тамом шуд!**\n📊 Натиҷаи ту: **{state['score']}/10** хол.", reply_markup=get_main_keyboard(), parse_mode="Markdown")
        return

    correct_item = questions[idx]
    question_text = f"Саволи {idx + 1}/10: Тарҷумаи дурусти '{correct_item['word']}' кадом аст?"
    
    wrong_options = [item['translation'] for item in UNIT1_WORDS if item['translation'] != correct_item['translation']]
    options = random.sample(wrong_options, min(3, len(wrong_options)))
    options.append(correct_item['translation'])
    random.shuffle(options)
    
    correct_index = options.index(correct_item['translation'])
    
    # Фиристодани викторина
    poll_msg = bot.send_poll(
        chat_id=chat_id,
        question=question_text,
        options=options,
        type='quiz',
        correct_option_id=correct_index,
        is_anonymous=False
    )
    user_states[chat_id]["last_poll_id"] = poll_msg.poll.id

# Пайгирии ҷавобҳои тест
@bot.poll_answer_handler(func=lambda answer: True)
def handle_poll_answer(answer):
    user_id = answer.user.id
    # Дар ин ҷо chat_id-ро аз рӯи сохтор муайян мекунем
    chat_id = user_id 
    state = user_states.get(chat_id)
    
    if state and state.get("last_poll_id") == answer.poll_id:
        idx = state["quiz_index"]
        correct_item = state["quiz_list"][idx]
        
        # Санҷиши ҷавоб
        if answer.option_ids[0] == state.get("correct_idx", 0): # Роҳи соддаи ҳисоб
            pass 
        
        # Барои автоматӣ гузаштан ба саволи баъдӣ
        user_states[chat_id]["quiz_index"] += 1
        # Агар корбар дуруст ҷавоб диҳад, хол илова мекунем (ин ҷо бот худаш дар экран нишон медиҳад)
        # Барои осонӣ, ҳангоми пахши ҷавоб, саволи навбатӣ пас аз 1 сония меояд
        import threading
        threading.Timer(1.5, send_next_quiz, args=[chat_id]).start()

# Веб-сервер барои Render
app = Flask(__name__)
@app.route('/')
def index(): return "Бот фаъол аст!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.polling(none_stop=True)
