import os
import sys
import random
from telebot import types

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

# Функсияи хондани калимаҳо аз файл
def load_words():
    words_dict = {}
    if os.path.exists("words.txt"):
        with open("words.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        u, w, t = parts
                        if u not in words_dict:
                            words_dict[u] = []
                        words_dict[u].append({"word": w, "translation": t})
    return words_dict

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📖 Луғат"), types.KeyboardButton("🎲 Тест"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "Салом! 👋 Хуш омадед ба боти **4000 Essential English Words**!\n\n"
        "👨‍💻 **Созанда:** Абдурраҳим\n"
        "Интихоб кунед 👇"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    chat_id = message.chat.id
    
    try:
        bot.delete_message(chat_id, message.message_id - 1)
    except:
        pass

    if message.text == "📖 Луғат":
        markup = types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        for i in range(1, 31):
            buttons.append(types.InlineKeyboardButton(f"Unit {i}", callback_data=f"show_unit_{i}"))
        markup.add(*buttons)
        bot.send_message(chat_id, "📚 **Кадом Юнитро хондан мехоҳӣ?**", reply_markup=markup)
        
    elif message.text == "🎲 Тест":
        db = load_words()
        all_combined = []
        for unit_words in db.values():
            all_combined.extend(unit_words)
            
        if not all_combined:
            bot.send_message(chat_id, "❌ Базаи калимаҳо холӣ аст. Аввал файлро пур кунед.")
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
        bot.send_message(chat_id, "🚀 Тести омехта аз 10 савол оғоз шуд!")
        send_next_quiz(chat_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('show_unit_'))
def handle_unit_selection(call):
    chat_id = call.message.chat.id
    unit_number = call.data.split('_')[2]
    db = load_words()
    
    if unit_number in db and db[unit_number]:
        response = f"📖 **Рӯйхати луғатҳои Unit {unit_number}:**\n\n"
        for i, item in enumerate(db[unit_number], 1):
            response += f"{i}. 🔤 **{item['word']}** = 🇹🇯 {item['translation']}\n"
    else:
        response = f"ℹ️ Калимаҳо барои **Unit {unit_number}** дар файли `words.txt` ёфт нашуданд!"

    bot.edit_message_text(response, chat_id, call.message.message_id, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

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

app = Flask(__name__)
@app.route('/')
def index(): return "Бот фаъол аст!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    bot.polling(none_stop=True)
