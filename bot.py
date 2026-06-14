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

user_states = {}

# Функсияи касбӣ барои хондани базаи калимаҳо аз файли words.txt
def load_words():
    words_dict = {}
    if os.path.exists("words.txt"):
        with open("words.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "|" not in line:
                    continue
                parts = line.split("|")
                if len(parts) == 4:
                    unit, word, trans, ex = parts
                    if unit not in words_dict:
                        words_dict[unit] = []
                    words_dict[unit].append({"word": word, "translation": trans, "example": ex})
    return words_dict

# Эҷоди тугмаҳои инлайнии Юнитҳо аз 1 то 30 (Танҳо дар даруни чат)
def get_inline_units_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(1, 31):
        buttons.append(types.InlineKeyboardButton(f"Unit {i}", callback_data=f"list_unit_{i}"))
    markup.add(*buttons)
    return markup

# Тугмаи оғози тест барои ҳамон Юнит
def get_inline_quiz_keyboard(unit_num):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"🎲 Оғози Тести Юнит {unit_num}", callback_data=f"start_quiz_{unit_num}"))
    markup.add(types.InlineKeyboardButton("📚 Рӯйхати Юнитҳо", callback_data="back_to_units"))
    return markup

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    welcome_msg = (
        "Салом! 👋 Хуш омадед ба боти калимаҳои англисӣ!\n\n"
        "👨‍💻 **Созанда:** Абдурраҳим\n\n"
        "📚 **Кадом Юнитро хондан мехоҳӣ? Интихоб кун:**"
    )
    # Тоза кардани клавиатураи оддии поёни экран (агар монда бошад)
    bot.send_message(message.chat.id, welcome_msg, reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "Интихоби Юнит 👇", reply_markup=get_inline_units_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    chat_id = call.message.chat.id
    data = call.data
    db = load_words()

    if data.startswith("list_unit_"):
        unit_number = data.split("_")[2]
        
        if unit_number in db and db[unit_number]:
            response = f"📖 **Рӯйхати луғатҳои Unit {unit_number} (Бо мисолҳо):**\n\n"
            for i, item in enumerate(db[unit_number], 1):
                response += f"{i}. 🔤 **{item['word']}** = 🇹🇯 {item['translation']}\n   📝 _Мисол:_ {item['example']}\n\n"
            
            bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=get_inline_quiz_keyboard(unit_number))
        else:
            bot.send_message(chat_id, f"ℹ️ Калимаҳо бо мисолҳояшон барои **Unit {unit_number}** дар файли `words.txt` ёфт нашуданд!", reply_markup=get_inline_units_keyboard())
        
        bot.answer_callback_query(call.id)

    elif data == "back_to_units":
        bot.send_message(chat_id, "📚 **Кадом Юнитро хондан мехоҳӣ?**", reply_markup=get_inline_units_keyboard())
        bot.answer_callback_query(call.id)

    elif data.startswith("start_quiz_"):
        unit_number = data.split("_")[2]
        unit_words = db.get(unit_number, [])
        
        if not unit_words:
            bot.send_message(chat_id, f"❌ Дар Unit {unit_number} калима барои тест ёфт нашуд.")
            bot.answer_callback_query(call.id)
            return

        shuffled_questions = random.sample(unit_words, min(10, len(unit_words)))
        
        all_words_pool = []
        for uw in db.values():
            all_words_pool.extend(uw)

        user_states[chat_id] = {
            "quiz_list": shuffled_questions,
            "quiz_index": 0,
            "score": 0,
            "last_poll_id": None,
            "correct_answer": "",
            "all_pool": all_words_pool
        }
        
        bot.send_message(chat_id, f"🚀 Тести махсус аз **Юнит {unit_number}** оғоз шуд ({len(shuffled_questions)} Савол)!")
        send_next_quiz(chat_id)
        bot.answer_callback_query(call.id)

def send_next_quiz(chat_id):
    state = user_states.get(chat_id)
    if not state:
        return
        
    idx = state["quiz_index"]
    questions = state["quiz_list"]
    all_pool = state["all_pool"]
    
    if idx >= len(questions):
        bot.send_message(
            chat_id, 
            f"🏁 **Тест ба охир расид!**\n📊 Натиҷаи ту: **{state['score']}/{len(questions)}** хол.", 
            reply_markup=get_inline_units_keyboard(), 
            parse_mode="Markdown"
        )
        return

    correct_item = questions[idx]
    question_text = f"Саволи {idx + 1}/{len(questions)}: Тарҷумаи дурусти калимаи '{correct_item['word']}' кадом аст?"
    
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
