import os
import sys
import random
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

# Базаи калимаҳо аз рӯи Юнитҳо (Маҳз аз рӯи китоби ту)
DATA_BASE = {
    "1": [
        {"word": "Agree", "translation": "Рози шудан"},
        {"word": "Alcohol", "translation": "Алкогол (нӯшокии спиртӣ)"},
        {"word": "Arrive", "translation": "Омадан, расидан"},
        {"word": "August", "translation": "Август"},
        {"word": "Boat", "translation": "Қаиқ, киштӣ"},
        {"word": "Breakfast", "translation": "Нонушта"},
        {"word": "Camera", "translation": "Камера, аксбардорак"},
        {"word": "Capital", "translation": "Пойтахт"},
        {"word": "Catch", "translation": "Доштан, қапидан"},
        {"word": "Duck", "translation": "Мурғобӣ"},
        {"word": "Enjoy", "translation": "Ҳаловат бурдан"},
        {"word": "Invite", "translation": "Даъват кардан"},
        {"word": "Love", "translation": "Дӯст доштан"},
        {"word": "Month", "translation": "Моҳ"},
        {"word": "Travel", "translation": "Саёҳат кардан"},
        {"word": "Typical", "translation": "Одатӣ, маъмулӣ"},
        {"word": "Visit", "translation": "Хабар гирифтан"},
        {"word": "Weather", "translation": "Обу ҳаво"},
        {"word": "Week", "translation": "Ҳафта"},
        {"word": "Wine", "translation": "Шароб (вино)"}
    ],
    "2": [
        {"word": "Adventure", "translation": "Саргузашт"},
        {"word": "Approach", "translation": "Наздик шудан"},
        {"word": "Carefully", "translation": "Боэҳтиёт"},
        {"word": "Chemical", "translation": "Моддаи chemical"},
        {"word": "Create", "translation": "Сохтан, эҷод кардан"},
        {"word": "Evil", "translation": "Бадӣ, ҷоҳил"},
        {"word": "Experiment", "translation": "Таҷриба, озмоиш"},
        {"word": "Kill", "translation": "Куштан"},
        {"word": "Laboratory", "translation": "Лаборатория"},
        {"word": "Laugh", "translation": "Ханда"}
    ],
    "3": [
        {"word": "Alien", "translation": "Мавҷудоти бегона"},
        {"word": "Among", "translation": "Дар байни"},
        {"word": "Chart", "translation": "Ҷадвал, диаграмма"},
        {"word": "Cloud", "translation": "Абр"},
        {"word": "Describe", "translation": "Тавсиф кардан"},
        {"word": "Fail", "translation": "Ноком шудан"},
        {"word": "Grade", "translation": "Баҳо, синф"},
        {"word": "Library", "translation": "Китобхона"},
        {"word": "Planet", "translation": "Сайёра"},
        {"word": "Solve", "translation": "Ҳал кардан"}
    ],
    "4": [
        {"word": "Avoid", "translation": "Дурӣ ҷӯстан"},
        {"word": "Behave", "translation": "Рафтори хуб кардан"},
        {"word": "Calm", "translation": "Ором"},
        {"word": "Concern", "translation": "Хавотирӣ"},
        {"word": "Expect", "translation": "Умед доштан"},
        {"word": "Habit", "translation": "Одат"},
        {"word": "Patient", "translation": "Босабр"},
        {"word": "Positive", "translation": "Мусбат"},
        {"word": "Punish", "translation": "Ҷазо додан"},
        {"word": "Village", "translation": "Деҳа"}
    ],
    "5": [
        {"word": "Active", "translation": "Фаъол"},
        {"word": "Adult", "translation": "Калонсол"},
        {"word": "Age", "translation": "Синну сол"},
        {"word": "Balance", "translation": "Мувозинат"},
        {"word": "Bike", "translation": "Велосипед"},
        {"word": "Choose", "translation": "Интихоб кардан"},
        {"word": "Doctor", "translation": "Духтур"},
        {"word": "Football", "translation": "Футбол"},
        {"word": "Game", "translation": "Бозӣ"},
        {"word": "Heart", "translation": "Дил"}
    ],
    "6": [
        {"word": "Apart", "translation": "Ҷудо, дур аз ҳам"},
        {"word": "Bilingual", "translation": "Дузабона"},
        {"word": "Completely", "translation": "Пурра, комилан"},
        {"word": "Mirror", "translation": "Оина"},
        {"word": "Natural", "translation": "Табиӣ"},
        {"word": "Sport", "translation": "Варзиш"},
        {"word": "Surprised", "translation": "Ҳайратзада"}
    ],
    "7": [
        {"word": "Allow", "translation": "Иҷозат додан"},
        {"word": "Announce", "translation": "Эълон кардан"},
        {"word": "Beside", "translation": "Дар наздӣ"},
        {"word": "Challenge", "translation": "Мушкилот"},
        {"word": "Expert", "translation": "Мутахассис"},
        {"word": "Famous", "translation": "Машҳур"},
        {"word": "Peace", "translation": "Тинҷӣ, сулҳ"},
        {"word": "Protect", "translation": "Муҳофизат кардан"}
    ],
    "8": [
        {"word": "Accept", "translation": "Қабул кардан"},
        {"word": "Arrange", "translation": "Танзим кардан"},
        {"word": "Attend", "translation": "Иштирок кардан"},
        {"word": "Chase", "translation": "Дунболгирӣ кардан"},
        {"word": "Huge", "translation": "Хеле калон"},
        {"word": "Necessary", "translation": "Зарурӣ"},
        {"word": "Satisfied", "translation": "Қонеъ, розӣ"}
    ],
    "9": [
        {"word": "Animal", "translation": "Ҳайвон"},
        {"word": "Bus", "translation": "Автобус"},
        {"word": "Cat", "translation": "Гурба"},
        {"word": "Dog", "translation": "Саг"},
        {"word": "Door", "translation": "Дар"},
        {"word": "Friend", "translation": "Дӯст"},
        {"word": "Hospital", "translation": "Беморхона"},
        {"word": "School", "translation": "Мактаб"}
    ],
    "10": [
        {"word": "Benefit", "translation": "Фоида, манфиат"},
        {"word": "Chance", "translation": "Имконият"},
        {"word": "Essential", "translation": "Муҳим, зарурӣ"},
        {"word": "Far", "translation": "Дур"},
        {"word": "Grass", "translation": "Алаф"},
        {"word": "Image", "translation": "Акс, тасвир"},
        {"word": "Proud", "translation": "Сарбаланд"},
        {"word": "Trouble", "translation": "Мушкилӣ"}
    ]
}

user_states = {}

# Клавиатураи асосӣ
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📖 Луғат"), types.KeyboardButton("🎲 Тест"))
    return markup

# Клавиатураи оддии Юнитҳо аз 1 то 30 (Дар поёни экран)
def get_units_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [types.KeyboardButton(f"Юнит {i}") for i in range(1, 31)]
    btn_back = types.KeyboardButton("⬅️ Ба Ортиқ (Меню)")
    markup.add(*buttons)
    markup.add(btn_back)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "Салом! 👋 Хуш омадед ба боти омӯзишии калимаҳо!\n\n"
        "👨‍💻 **Созанда:** Абдурраҳим\n"
        "Интихоб кун 👇"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_bot_logic(message):
    chat_id = message.chat.id
    text = message.text

    if text == "📖 Луғат":
        # Намоиши менюи оддии Юнитҳо дар поёни экран
        bot.send_message(chat_id, "📚 **Кадом Юнитро хондан мехоҳӣ? Интихоб кун:**", reply_markup=get_units_keyboard())

    elif text == "⬅️ Ба Ортиқ (Меню)":
        # Баргашт ба менюи асосӣ
        bot.send_message(chat_id, "🏠 Ба менюи асосӣ баргаштид:", reply_markup=get_main_keyboard())

    elif text.startswith("Юнит "):
        # Гирифтани рақами Юнит аз матни тугма
        unit_number = text.split(" ")[1]
        
        if unit_number in DATA_BASE and DATA_BASE[unit_number]:
            response = f"📖 **Рӯйхати луғатҳои Unit {unit_number}:**\n\n"
            for i, item in enumerate(DATA_BASE[unit_number], 1):
                response += f"{i}. 🔤 **{item['word']}** = 🇹🇯 {item['translation']}\n"
        else:
            response = f"ℹ️ Калимаҳо барои **Unit {unit_number}** ба наздикӣ илова карда мешаванд!"
        
        # Калимаҳоро ҳамчун паёми нав мефиристем (кӯҳнаҳо тоза намешаванд ва анимация нест)
        bot.send_message(chat_id, response, parse_mode="Markdown")

    elif text == "🎲 Тест":
        # Омода кардани саволҳо аз ҳамаи калимаҳои мавҷуда
        all_combined = []
        for unit_words in DATA_BASE.values():
            all_combined.extend(unit_words)
            
        if not all_combined:
            bot.send_message(chat_id, "❌ Базаи калимаҳо холӣ аст.")
            return

        shuffled_questions = random.sample(all_combined, min(10, len(all_combined)))
        user_states[chat_id] = {
            "quiz_list": shuffled_questions,
            "quiz_index": 0,
            "score": 0,
            "last_poll_id": None,
            "correct_answer": "",
            "all_pool": all_combined
        }
        bot.send_message(chat_id, "🚀 Тести омехта аз 10 савол оғоз шуд!", reply_markup=get_main_keyboard())
        send_next_quiz(chat_id)

def send_next_quiz(chat_id):
    state = user_states.get(chat_id)
    if not state:
        return
        
    idx = state["quiz_index"]
    questions = state["quiz_list"]
    all_pool = state["all_pool"]
    
    if idx >= len(questions):
        bot.send_message(chat_id, f"🏁 **Тест ба охир расид!**\n📊 Натиҷаи ту: **{state['score']}/10** хол.", reply_markup=get_main_keyboard(), parse_mode="Markdown")
        return

    correct_item = questions[idx]
    question_text = f"Саволи {idx + 1}/10: Тарҷумаи дурусти калимаи '{correct_item['word']}' кадом аст?"
    
    wrong_options = [item['translation'] for item in all_pool if item['translation'] != correct_item['translation']]
    wrong_options = list(set(wrong_options))
    
    options = random.sample(wrong_options, min(3, len(wrong_options)))
    options.append(correct_item['translation'])
    random.shuffle(options)
    
    correct_index = options.index(correct_item['translation'])
    
    user_states[chat_id]["correct_answer"] = correct_item['translation']
    user_states[chat_id]["options_list"] = options
    
    poll_msg = bot.send_poll(
        chat_id=chat_id,
        question=question_text,
        options=options,
        type='quiz',
        correct_option_id=correct_index,
        is_anonymous=False
    )
    user_states[chat_id]["last_poll_id"] = poll_msg.poll.id

@bot.poll_answer_handler(func=lambda answer: True)
def handle_poll_answer(answer):
    user_id = answer.user.id
    chat_id = user_id
    state = user_states.get(chat_id)
    
    if state and state.get("last_poll_id") == answer.poll_id:
        options = state.get("options_list", [])
        chosen_option_id = answer.option_ids[0]
        chosen_translation = options[chosen_option_id]
        
        if chosen_translation == state.get("correct_answer"):
            user_states[chat_id]["score"] += 1
            
        user_states[chat_id]["quiz_index"] += 1
        
        import threading
        threading.Timer(1.0, send_next_quiz, args=[chat_id]).start()

# Веб-сервер барои Render
app = Flask(__name__)
@app.route('/')
def index(): return "Бот фаъол аст!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.polling(none_stop=True)
