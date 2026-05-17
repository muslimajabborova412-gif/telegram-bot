import os
import random
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'
WEBHOOK_URL = 'https://telegram-bot-quiz-3cqc.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

QUIZ_DATA = {
    "A1 (Beginner)": [
        {"q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "Бо ҷонишини I ҳамеша am мешавад."},
        {"q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "Барои He/She/It суффикси -s илова мешавад."},
        {"q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "Бо you феъли ёвари do меояд."},
        {"q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "Инкор барои They бо don't мешавад."},
        {"q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "Барои He феъл бо -s меояд."}
    ],
    "A2 (Elementary)": [
        {"q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "Гузаштаи go мешавад went."},
        {"q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "Муқоиса бо суффикси -er сохта мешавад."}
    ]
}

USER_DATA = {}

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook_setup():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + '/' + TOKEN)
    return "Webhook configured! 🚀"

@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_id = message.from_user.id
    USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": [], "state": "CHOOSE_LEVEL"}
    
    welcome_text = "👋 Welcome to the English Quiz Bot!\n\nPlease, choose your level:"
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("A1 (Beginner)"))
    markup.add(KeyboardButton("A2 (Elementary)"))
    
    bot.send_message(user_id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in USER_DATA:
        start_quiz(message)
        return

    state = USER_DATA[user_id].get("state")

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
            
            bot.send_message(user_id, f"🏁 You have chosen {text}. The quiz has started!", reply_markup=ReplyKeyboardRemove())
            send_question(user_id)

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

def send_question(user_id):
    current_q = USER_DATA[user_id]["current_q"]
    q_list = USER_DATA[user_id]["questions"]

    if current_q >= len(q_list):
        show_results(user_id)
        return

    question = q_list[current_q]
    
    # Матни оддӣ бе форматкунии Markdown, то ки хатогӣ нашавад
    text = f"Question {current_q + 1} of {len(q_list)}:\n\n{question['q']}"
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in question["options"]:
        markup.add(KeyboardButton(opt))
        
    bot.send_message(user_id, text, reply_markup=markup)

def show_results(user_id):
    score = USER_DATA[user_id]["score"]
    wrongs = USER_DATA[user_id]["wrong_answers"]
    total = len(USER_DATA[user_id]["questions"])
    
    result_text = f"🏁 The quiz is over!\n📊 Your score: {score} out of {total}\n\n"
    
    if wrongs:
        result_text += "🛠 Таҳлили хатогиҳо:\n\n"
        for idx, w in enumerate(wrongs):
            result_text += f"❌ Хатогии {idx+1}:\n❓ Савол: {w['q']}\n✅ Ҷавоб: {w['correct']}\n💡 Қоида: {w['rule']}\n\n"
            
    result_text += "\n🔄 Press /start to try again."
    USER_DATA[user_id]["state"] = "CHOOSE_LEVEL"
    bot.send_message(user_id, result_text, reply_markup=ReplyKeyboardRemove())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
