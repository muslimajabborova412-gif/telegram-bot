import os
import random
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'
WEBHOOK_URL = 'https://telegram-bot-quiz-3cqc.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# БАЗАИ БЕШТАРӢ АЗ САВОЛҲО БАРОИ РАНДОМ ШУДАН
QUIZ_DATA = {
    "A1 (Beginner)": [
        {"q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "Бо ҷонишини 'I' ҳамеша 'am' мешавад."},
        {"q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "Барои He/She/It феъл суффикси '-s' мегирад."},
        {"q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "Барои 'you' феъли ёвари 'do' лозим аст."},
        {"q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "Инкор барои They бо 'don't' мешавад."},
        {"q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "Барои He феъл бо '-s' меояд."},
        {"q": "This is ___ apple.", "options": ["an", "a", "the"], "correct": "an", "rule": "Пеш аз овози садонок 'an' меояд."},
        {"q": "We ___ happy today.", "options": ["are", "am", "is"], "correct": "are", "rule": "Барои шакли ҷамъ 'are' истифода мешавад."},
        {"q": "What is ___ name?", "options": ["your", "you", "yours"], "correct": "your", "rule": "Ҷонишини соҳибии 'your' (номи ту) пеш аз исм меояд."},
        {"q": "Look at ___ birds in the sky.", "options": ["those", "these", "this"], "correct": "those", "rule": "'Those' барои ашёи ҷамъи дур аст."},
        {"q": "I have ___ brothers.", "options": ["two", "to", "too"], "correct": "two", "rule": "Калимаи 'two' шумораи 2-ро англиси аст."},
        {"q": "How ___ are you? I'm 20.", "options": ["old", "age", "years"], "correct": "old", "rule": "Барои пурсидани синну сол 'How old' мегӯянд."},
        {"q": "Goodbye! See you ___.", "options": ["later", "late", "now"], "correct": "later", "rule": "'See you later' ибораи хайрбодӣ аст."}
    ],
    "A2 (Elementary)": [
        {"q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "Гузаштаи феъли 'go' мешавад 'went'."},
        {"q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "Муқоисаи ду чиз бо '-er' сохта мешавад."},
        {"q": "Have you ___ English before?", "options": ["study", "studied", "studying"], "correct": "studied", "rule": "Пас аз have/has шакли 3-юми феъл (V3) меояд."},
        {"q": "Listen! The baby ___.", "options": ["cries", "is crying", "cried"], "correct": "is crying", "rule": "Амал ҳозир рафта истодааст (Present Continuous)."},
        {"q": "There ___ some milk in the fridge.", "options": ["is", "are", "any"], "correct": "is", "rule": "Шир исми ҳисобнашаванда аст, бинобар ин 'is' мешавад."},
        {"q": "I ___ a new movie last night.", "options": ["watched", "watch", "watching"], "correct": "watched", "rule": "'Last night' замони гузашта аст."},
        {"q": "This car is the ___ in the shop.", "options": ["most expensive", "more expensive", "expensive"], "correct": "most expensive", "rule": "Дараҷаи олии сифат бо 'the most' сохта мешавад."},
        {"q": "She speaks English ___.", "options": ["well", "good", "bad"], "correct": "well", "rule": "Барои тасвири феъл зарфи 'well' истифода мешавад."}
    ],
    "B1 (Intermediate)": [
        {"q": "If it rains, we ___ stay at home.", "options": ["will", "would", "shall"], "correct": "will", "rule": "First Conditional: Шарти ҳозира + Натиҷаи оянда (Will)."},
        {"q": "The book ___ written by him in 2024.", "options": ["was", "is", "were"], "correct": "was", "rule": "Passive Voice дар замони гузашта: was + V3."},
        {"q": "I look forward to ___ you.", "options": ["seeing", "see", "seen"], "correct": "seeing", "rule": "Ибораи 'look forward to' Герундий (-ing)-ро талаб мекунад."},
        {"q": "I wish I ___ more time to study now.", "options": ["had", "have", "will have"], "correct": "had", "rule": "Пас аз 'I wish' замони гузашта (Past Simple) истифода мешавад."},
        {"q": "By the time you arrive, the train ___ left.", "options": ["will have", "will", "has"], "correct": "will have", "rule": "Future Perfect барои амале, ки то вақти муайян дар оянда иҷро мешавад."}
    ],
    "B2 (Upper-Intermediate)": [
        {"q": "She avoids ___ sugar to lose weight.", "options": ["eating", "to eat", "eat"], "correct": "eating", "rule": "Феъли 'avoid' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"q": "You ___ look at the sun; it damages your eyes.", "options": ["mustn't", "don't have to", "needn't"], "correct": "mustn't", "rule": "'Mustn't' барои манъ кардани амали хатарнок истифода мешавад."}
    ],
    "C1 (Advanced)": [
        {"q": "Hardly ___ entered the room when the phone rang.", "options": ["had I", "I had", "did I"], "correct": "had I", "rule": "Инверсия: пас аз Hardly аввал феъли ёвар (had) меояд."},
        {"q": "If I had studied harder, I ___ a degree now.", "options": ["would have", "would have had", "will have"], "correct": "would have", "rule": "Mixed Conditional: Шарти гузашта + Натиҷаи ҳозира."}
    ]
}

ALL_USERS = set()
ACTIVE_USERS = set()
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
    ALL_USERS.add(user_id)
    ACTIVE_USERS.add(user_id)
    
    USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": []}
    
    welcome_text = (
        "👋 **Welcome to the English Quiz Bot!**\n\n"
        "👤 **Developer:** Abdurahim Sheraliev\n"
        "📊 **Системаи Рандом:** Саволҳо барои ҳар як шахс ба таври тасодуфӣ ва гуногун меоянд!\n"
        "🎯 Дар охир фоизи дониши урувини шумо ҳисоб карда мешавад.\n\n"
        "💡 Лутфан, дараҷаро интихоб кунед:"
    )
    
    markup = InlineKeyboardMarkup()
    for lvl in QUIZ_DATA.keys():
        markup.add(InlineKeyboardButton(lvl, callback_data=f"lvl:{lvl}"))
        
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['stat'])
def show_stat(message):
    bot.send_message(
        message.from_user.id,
        f"📊 **Статистика:**\n\n👥 Ҷамъи корбарон: **{len(ALL_USERS)}**\n🟢 Фаъолон (Онлайн): **{len(ACTIVE_USERS)}**",
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = call.data
    ACTIVE_USERS.add(user_id)

    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": []}

    # ИНТИХОБИ УРУВИН ВА РАНДОМ КАРДАНИ САВОЛҲО
    if data.startswith("lvl:"):
        level = data.split(":")[1]
        USER_DATA[user_id]["level"] = level
        
        all_q = [item.copy() for item in QUIZ_DATA[level]]
        random.shuffle(all_q)  # Омехта кардани саволҳо барои ҳар як кас алоҳида
        
        # Агар саволҳо дар база кам бошанд, ҳамаашро мегирем, вагарна маҳдуд ба 10 савол
        total_to_take = min(10, len(all_q))
        USER_DATA[user_id]["questions"] = all_q[:total_to_take]
        USER_DATA[user_id]["current_q"] = 0
        USER_DATA[user_id]["score"] = 0
        USER_DATA[user_id]["wrong_answers"] = []
        
        bot.edit_message_text(f"🏁 **You have chosen {level}. The quiz has started! Total: {total_to_take} random questions.**", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        send_question(user_id, call.message.chat.id)

    # ҶАВОБ БА САВОЛҲО
    elif data.startswith("ans:"):
        _, is_correct, ans_idx = data.split(":")
        current_q_idx = USER_DATA[user_id]["current_q"]
        q_list = USER_DATA[user_id]["questions"]
        
        if current_q_idx < len(q_list):
            current_question = q_list[current_q_idx]
            chosen_option = current_question["options"][int(ans_idx)]
            
            if is_correct == "1":
                USER_DATA[user_id]["score"] += 1
                # Эффекти ҷавоби дуруст дар худи тугма
                bot.answer_callback_query(call.id, "✅ Correct! True", show_alert=False)
            else:
                USER_DATA[user_id]["wrong_answers"].append({
                    "q": current_question["q"],
                    "chosen": chosen_option,
                    "correct": current_question["correct"],
                    "rule": current_question["rule"]
                })
                bot.answer_callback_query(call.id, f"❌ Wrong! Correct is: {current_question['correct']}", show_alert=False)
                
            USER_DATA[user_id]["current_q"] += 1
            # Тоза кардани паёми кӯҳна барои тозагии чат
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            send_question(user_id, call.message.chat.id)

def send_question(user_id, chat_id):
    current_q = USER_DATA[user_id]["current_q"]
    q_list = USER_DATA[user_id]["questions"]

    if current_q >= len(q_list):
        show_results(user_id, chat_id)
        return

    question = q_list[current_q]
    text = f"❓ **Question {current_q + 1}/{len(q_list)}:**\n\n`{question['q']}`"
    
    markup = InlineKeyboardMarkup()
    for idx, opt in enumerate(question["options"]):
        is_correct = "1" if opt == question["correct"] else "0"
        markup.add(InlineKeyboardButton(opt, callback_data=f"ans:{is_correct}:{idx}"))
        
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

def show_results(user_id, chat_id):
    score = USER_DATA[user_id]["score"]
    wrongs = USER_DATA[user_id]["wrong_answers"]
    total = len(USER_DATA[user_id]["questions"])
    
    # ҲИСОВИ ФОИЗИ УРУВИН
    percentage = int((score / total) * 100) if total > 0 else 0
    
    result_text = (
        f"🏁 **The quiz is over!**\n\n"
        f"📊 Your score: **{score} out of {total}**\n"
        f"🎯 Урувини дониши шумо: **{percentage}%**\n\n"
    )
    
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
        result_text += "🎉 **Awesome! Баракалоҳ! 100% ҷавоби дуруст!**"

    result_text += "\n🔄 Нависед /start барои аз нав оғоз кардан."
    bot.send_message(chat_id, result_text, parse_mode="Markdown")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
