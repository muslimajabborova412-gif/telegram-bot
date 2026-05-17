import os
import random
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'
WEBHOOK_URL = 'https://telegram-bot-quiz-3cqc.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# БАЗАИ БУЗУРГИ САВОЛҲО БАРОИ ГЕНЕРАТСИЯИ РАНДОМ
QUIZ_DATA = {
    "A1 (Beginner)": [
        {"id": 1, "q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "Бо ҷонишини 'I' ҳамеша 'am' мешавад."},
        {"id": 2, "q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "Барои He/She/It феъл суффикси '-s' мегирак."},
        {"id": 3, "q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "Барои 'you' феъли ёвари 'do' лозим аст."},
        {"id": 4, "q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "Инкор барои They бо 'don't' мешавад."},
        {"id": 5, "q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "Барои He феъл бо '-s' меояд."},
        {"id": 6, "q": "This is ___ apple.", "options": ["an", "a", "the"], "correct": "an", "rule": "Пеш аз овози садонок 'an' меояд."},
        {"id": 7, "q": "We ___ happy today.", "options": ["are", "am", "is"], "correct": "are", "rule": "Барои шакли ҷамъ 'are' истифода мешавад."},
        {"id": 8, "q": "What is ___ name?", "options": ["your", "you", "yours"], "correct": "your", "rule": "Ҷонишини соҳибии 'your' пеш аз исм меояд."},
        {"id": 9, "q": "Look at ___ birds in the sky.", "options": ["those", "these", "this"], "correct": "those", "rule": "'Those' барои ашёи ҷамъи дур аст."},
        {"id": 10, "q": "I have ___ brothers.", "options": ["two", "to", "too"], "correct": "two", "rule": "Калимаи 'two' шумораи 2 аст."},
        {"id": 11, "q": "How ___ are you? I'm 20.", "options": ["old", "age", "years"], "correct": "old", "rule": "Барои синну сол 'How old' мегӯянд."},
        {"id": 12, "q": "Goodbye! See you ___.", "options": ["later", "late", "now"], "correct": "later", "rule": "'See you later' ибораи хайрбодӣ аст."}
    ],
    "A2 (Elementary)": [
        {"id": 13, "q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "Гузаштаи феъли 'go' мешавад 'went'."},
        {"id": 14, "q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "Муқоисаи ду чиз бо '-er' сохта мешавад."},
        {"id": 15, "q": "Have you ___ English before?", "options": ["study", "studied", "studying"], "correct": "studied", "rule": "Пас аз have/has шакли 3-юми феъл (V3) меояд."},
        {"id": 16, "q": "Listen! The baby ___.", "options": ["cries", "is crying", "cried"], "correct": "is crying", "rule": "Амал ҳозир рафта истодааст (Present Continuous)."},
        {"id": 17, "q": "There ___ some milk in the fridge.", "options": ["is", "are", "any"], "correct": "is", "rule": "Шир исми ҳисобнашаванда аст, бинобар ин 'is' мешавад."},
        {"id": 18, "q": "I ___ a new movie last night.", "options": ["watched", "watch", "watching"], "correct": "watched", "rule": "'Last night' замони гузашта аст."},
        {"id": 19, "q": "This car is the ___ in the shop.", "options": ["most expensive", "more expensive", "expensive"], "correct": "most expensive", "rule": "Дараҷаи олии сифат бо 'the most' сохта мешавад."},
        {"id": 20, "q": "She speaks English ___.", "options": ["well", "good", "bad"], "correct": "well", "rule": "Барои тасвири феъл зарфи 'well' истифода мешавад."}
    ],
    "B1 (Intermediate)": [
        {"id": 21, "q": "If it rains, we ___ stay at home.", "options": ["will", "would", "shall"], "correct": "will", "rule": "First Conditional: Шарти ҳозира + Натиҷаи оянда (Will)."},
        {"id": 22, "q": "The book ___ written by him in 2024.", "options": ["was", "is", "were"], "correct": "was", "rule": "Passive Voice дар замони гузашта: was + V3."},
        {"id": 23, "q": "I look forward to ___ you.", "options": ["seeing", "see", "seen"], "correct": "seeing", "rule": "Ибораи 'look forward to' Герундий (-ing)-ро талаб мекунад."},
        {"id": 24, "q": "I wish I ___ more time to study now.", "options": ["had", "have", "will have"], "correct": "had", "rule": "Пас аз 'I wish' замони гузашта (Past Simple) истифода мешавад."},
        {"id": 25, "q": "By the time you arrive, the train ___ left.", "options": ["will have", "will", "has"], "correct": "will have", "rule": "Future Perfect барои амале, ки то вақти муайян дар оянда иҷро мешавад."}
    ],
    "B2 (Upper-Intermediate)": [
        {"id": 26, "q": "She avoids ___ sugar to lose weight.", "options": ["eating", "to eat", "eat"], "correct": "eating", "rule": "Феъли 'avoid' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"id": 27, "q": "You ___ look at the sun; it damages your eyes.", "options": ["mustn't", "don't have to", "needn't"], "correct": "mustn't", "rule": "'Mustn't' барои манъ кардани амали хатарнок истифода мешавад."}
    ],
    "C1 (Advanced)": [
        {"id": 28, "q": "Hardly ___ entered the room when the phone rang.", "options": ["had I", "I had", "did I"], "correct": "had I", "rule": "Инверсия: пас аз Hardly аввал феъли ёвар (had) меояд."},
        {"id": 29, "q": "If I had studied harder, I ___ a degree now.", "options": ["would have", "would have had", "will have"], "correct": "would have", "rule": "Mixed Conditional: Шарти гузашта + Натиҷаи ҳозира."}
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
    
    welcome_text = (
        "👋 **Welcome to the English Quiz Bot!**\n\n"
        "👤 **Developer:** Abdurahim Sheraliev\n"
        "📚 **Маълумот:** Ин бот ба ту кӯмак мекунад, ки дараҷаи забони англисии худро бисанҷӣ.\n\n"
        "💡 Лутфан, дараҷаро интихоб кунед:"
    )
    
    markup = InlineKeyboardMarkup()
    for lvl in QUIZ_DATA.keys():
        markup.add(InlineKeyboardButton(lvl, callback_data=f"setup_lvl:{lvl}"))
        
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

    # 1. ТАНЗИМИ ТЕСТИ РАНДОМ БАРОИ КОРБАР
    if data.startswith("setup_lvl:"):
        level = data.split(":")[1]
        
        all_q = [item.copy() for item in QUIZ_DATA[level]]
        random.shuffle(all_q)  # Ба ҳар кас саволҳои комилан рандом ва дигар меоянд!
        
        chosen_questions = all_q[:10]  # Натиҷаи 10 саволи тасодуфӣ
        
        USER_DATA[user_id] = {
            "level": level,
            "questions": chosen_questions,
            "answers": {}, # Барои сабти ҷавобҳои интихобкардаи корбар {савол_id: интихоб}
            "msg_id": call.message.message_id
        }
        
        render_test_page(user_id, call.message.chat.id, call.message.message_id)

    # 2. КЛИК КАРДАНИ ВАРИАНТҲОИ ТЕСТ
    elif data.startswith("pick:"):
        _, q_id, opt_idx = data.split(":")
        q_id = int(q_id)
        opt_idx = int(opt_idx)
        
        if user_id in USER_DATA:
            # Ҷавоби интихобшударо сабт мекунем
            USER_DATA[user_id]["answers"][q_id] = opt_idx
            # Паёми тестро нав мекунем, то нишон диҳад, ки кадом тугма клик шуд
            render_test_page(user_id, call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id, "Қайд карда шуд!")

    # 3. ТУГМАИ САНҶИДАН (SUBMIT)
    elif data == "submit_test":
        if user_id in USER_DATA:
            questions = USER_DATA[user_id]["questions"]
            user_answers = USER_DATA[user_id]["answers"]
            
            score = 0
            wrongs = []
            
            for q in questions:
                chosen_idx = user_answers.get(q["id"])
                if chosen_idx is not None:
                    chosen_text = q["options"][chosen_idx]
                    if chosen_text == q["correct"]:
                        score += 1
                    else:
                        wrongs.append({
                            "q": q["q"],
                            "chosen": chosen_text,
                            "correct": q["correct"],
                            "rule": q["rule"]
                        })
                else:
                    # Агар саволро умуман ҷавоб надода бошад
                    wrongs.append({
                        "q": q["q"],
                        "chosen": "Ҷавоб дода нашудааст ❌",
                        "correct": q["correct"],
                        "rule": q["rule"]
                    })
            
            total = len(questions)
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
            
            # Паёми тестро нест карда, натиҷаи умумиро мебарорем
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, result_text, parse_mode="Markdown")

def render_test_page(user_id, chat_id, message_id):
    """Тамоми 10 саволро дар як блок бо нишондиҳандаи интихобҳо месозад"""
    data = USER_DATA[user_id]
    questions = data["questions"]
    user_answers = data["answers"]
    
    # Сохтани матни умумии паём, ки тамоми 10 саволро якбора нишон медиҳад
    text = f"📝 **English Quiz — Level: {data['level']}**\n"
    text += "Ҳамаи саволҳоро ҷавоб диҳед ва дар таг тугмаи 'Санҷидан'-ро пахш кунед:\n\n"
    
    markup = InlineKeyboardMarkup()
    
    for idx, q in enumerate(questions):
        chosen_idx = user_answers.get(q["id"])
        
        # Ба матни паём илова кардани саволҳо
        if chosen_idx is not None:
            text += f"{idx+1}. `{q['q']}` ➔ (Қайд шуд: {q['options'][chosen_idx]})\n"
        else:
            text += f"{idx+1}. `{q['q']}` ➔ (Интихоб кунед ⏳)\n"
            
        # Сохтани қатори тугмаҳо барои ин савол
        row_buttons = []
        for opt_idx, opt in enumerate(q["options"]):
            # Агар ин вариант интихоб шуда бошад, ба он нишони 🔹 мемонем
            btn_text = f"🔹 {opt}" if chosen_idx == opt_idx else opt
            row_buttons.append(InlineKeyboardButton(f"{idx+1}: {btn_text}", callback_data=f"pick:{q['id']}:{opt_idx}"))
        
        markup.row(*row_buttons)
        
    # Дар худи таги ҳамаи саволҳо тугмаи ягонаи САНҶИДАН-ро мемонем
    markup.add(InlineKeyboardButton("📊 Санҷидан (Submit Result)", callback_data="submit_test"))
    
    # Навсозии паём бе нест шудан
    bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
