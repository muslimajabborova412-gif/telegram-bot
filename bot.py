import os
import threading
import random
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# ✅ ТОКЕНИ НАВИ ТУ
TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "English Quiz Bot is running perfectly! 🚀"

# БАЗАИ САВОЛҲО
QUIZ_DATA = {
    "A1 (Beginner)": [
        {"q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "Бо ҷонишини 'I' (ман) ҳамеша феъли то-be 'am' истифода мешавад."},
        {"q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "Дар замони Present Simple барои He, She, It ба охири feъл суффикси '-s' илова мешавад."},
        {"q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "Бо ҷонишини 'you' феъли ёвари 'do' истифода мешавад."},
        {"q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "Инкор барои шакли ҷамъ (They) бо ёрии 'don't' сохта мешавад."},
        {"q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "Дар Present Simple барои He/She/It ба feъл '-s' илова мешавад."}
    ],
    "A2 (Elementary)": [
        {"q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "Калимаи 'Yesterday' нишон медиҳад, ки замон Past Simple аст. Шакли гузаштаи 'go' -> 'went' мешавад."},
        {"q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "Барои муқоисаи ду шахс ба сифат суффикси '-er' илова карда мешавад."},
        {"q": "Have you ___ English before?", "options": ["study", "studied", "studying"], "correct": "studied", "rule": "Дар замони Present Perfect пас аз 'have/has' шакли сеюми феъл (V3) меояд."},
        {"q": "Listen! The baby ___.", "options": ["cries", "is crying", "cried"], "correct": "is crying", "rule": "Амал дар ҳамин сония рафта истодааст (Present Continuous)."},
        {"q": "There ___ some milk in the fridge.", "options": ["is", "are", "any"], "correct": "is", "rule": "Исми 'milk' ҳисобнашаванда аст, бинобар ин 'is' мешавад."}
    ],
    "B1 (Intermediate)": [
        {"q": "If it rains, we ___ stay at home.", "options": ["will", "would", "shall"], "correct": "will", "rule": "First Conditional: Шарти ҳозира (Present) + Натиҷаи оянда (Will)."},
        {"q": "The book ___ written by him in 2024.", "options": ["is", "was", "were"], "correct": "was", "rule": "Passive Voice дар замони гузашта: Шакли танҳо + was + V3."},
        {"q": "I look forward to ___ you.", "options": ["see", "seeing", "seen"], "correct": "seeing", "rule": "Ибораи 'look forward to' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"q": "I wish I ___ more time to study.", "options": ["have", "had", "will have"], "correct": "had", "rule": "Пас аз сохтори 'I wish' барои замони ҳозира замони гузашта (Past Simple) истифода мешавад."},
        {"q": "By the time you arrive, the train ___ left.", "options": ["will", "will have", "has"], "correct": "will have", "rule": "Future Perfect: Амале, ки то вақти муайян дар оянда ба охир мерасад."}
    ]
}

USER_DATA = {}

@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_id = message.from_user.id
    USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": [], "state": "CHOOSE_LEVEL"}
    
    welcome_text = (
        "👋 Welcome to the English Quiz Bot!\n\n"
        "👤 **Developer:** Abdurahim Sheraliev\n"
        "📚 This bot will help you test your English language levels.\n"
        "📝 At the end, your mistakes will be explained in Tajik.\n\n"
        "💡 Please, choose your level:"
    )
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("A1 (Beginner)"))
    markup.add(KeyboardButton("A2 (Elementary)"))
    markup.add(KeyboardButton("B1 (Intermediate)"))
    
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in USER_DATA:
        start_quiz(message)
        return

    state = USER_DATA[user_id].get("state")

    # Интихоби дараҷа
    if state == "CHOOSE_LEVEL":
        if text in QUIZ_DATA:
            USER_DATA[user_id]["level"] = text
            all_q = [item.copy() for item in QUIZ_DATA[text]]
            random.shuffle(all_q)
            
            USER_DATA[user_id]["questions"] = all_q
            USER_DATA[user_id]["current_q"] = 0
            USER_DATA[user_id]["score"] = 0
            USER_DATA[user_id]["wrong_answers"] = []
            USER_DATA[user_id]["state"] = "QUIZ_RUNNING"
            
            bot.send_message(user_id, f"🏁 You have chosen **{text}**. The quiz has started!", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
            send_question(user_id)
        else:
            bot.send_message(user_id, "Please, choose a level from the keyboard buttons below.")

    # Раванди тест
    elif state == "QUIZ_RUNNING":
        current_q_idx = USER_DATA[user_id]["current_q"]
        q_list = USER_DATA[user_id]["questions"]
        
        if current_q_idx < len(q_list):
            current_question = q_list[current_q_idx]
            
            if text in current_question["options"]:
                if text == current_question["correct"]:
                    USER_DATA[user_id]["score"] += 1
                else:
                    USER_DATA[user_id]["wrong_answers"].append({
                        "q": current_question["q"],
                        "chosen": text,
                        "correct": current_question["correct"],
                        "rule": current_question["rule"]
                    })
                
                USER_DATA[user_id]["current_q"] += 1
                send_question(user_id)
            else:
                bot.send_message(user_id, "Please, select one of the provided options.")

def send_question(user_id):
    current_q = USER_DATA[user_id]["current_q"]
    q_list = USER_DATA[user_id]["questions"]

    if current_q >= len(q_list):
        show_results(user_id)
        return

    question = q_list[current_q]
    text = f"❓ **Question {current_q + 1}/{len(q_list)}:**\n\n{question['q']}"
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in question["options"]:
        markup.add(KeyboardButton(opt))
        
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

def show_results(user_id):
    score = USER_DATA[user_id]["score"]
    wrongs = USER_DATA[user_id]["wrong_answers"]
    total = len(USER_DATA[user_id]["questions"])
    
    result_text = f"🏁 **The quiz is over!**\n\n📊 Your score: **{score} out of {total}**\n\n"
    
    if wrongs:
        result_text += "🛠 **Таҳлили хатогиҳо ва қоидаҳо (бо забони тоҷикӣ):**\n\n"
        for idx, w in enumerate(wrongs):
            result_text += (
                f"❌ *Хатогии {idx+1}:*\n"
                f"❓ Савол: `{w['q']}`\n"
                f"🔻 Интихоби шумо: {w['chosen']}\n"
                f"✅ Ҷавоби дуруст: *{w['correct']}*\n"
                f"💡 **Қоида:** {w['rule']}\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            )
    else:
        result_text += f"🎉 Awesome! You answered all {total} questions correctly!"

    result_text += "\n🔄 Press /start to try again."
    USER_DATA[user_id]["state"] = "CHOOSE_LEVEL"
    bot.send_message(user_id, result_text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot started successfully...")
    bot.remove_webhook()
    bot.infinity_polling()
