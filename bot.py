import os
import random
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'
WEBHOOK_URL = 'https://telegram-bot-quiz-3cqc.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# БАЗАИ МУКАММАЛИ САВОЛҲО (Аз А1 то С1)
QUIZ_DATA = {
    "A1 (Beginner)": [
        {"q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "Бо ҷонишини 'I' (ман) ҳамеша 'am' истифода мешавад."},
        {"q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "Дар замони Present Simple барои He/She/It ба охири феъл 's' илова мешавад."},
        {"q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "Барои сохтани савол бо 'you' феъли ёвари 'do' лозим аст."},
        {"q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "Инкори ҷумла барои They бо 'don't' сохта мешавад."},
        {"q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "Барои ҷонишини 'He' феъл суффикси 's' мегирад."},
        {"q": "This is ___ apple.", "options": ["an", "a", "the"], "correct": "an", "rule": "Пеш аз исмҳое, ки бо овози садонок сар мешаванд, артикли 'an' меояд."},
        {"q": "We ___ happy today.", "options": ["are", "am", "is"], "correct": "are", "rule": "Барои ҷонишини шакли ҷамъ (We) феъли 'are' истифода мешавад."},
        {"q": "What is ___ name?", "options": ["your", "you", "yours"], "correct": "your", "rule": "Ҷонишини соҳибии 'your' (номи ту) пеш аз исм меояд."},
        {"q": "Look at ___ birds in the sky over there.", "options": ["those", "these", "this"], "correct": "those", "rule": "'Those' барои нишон додани ашёҳои ҷамъи дур истифода мешавад."},
        {"q": "I have ___ brothers.", "options": ["two", "to", "too"], "correct": "two", "rule": "Калимаи 'two' маънои шумораи 2-ро дорад."}
    ],
    "A2 (Elementary)": [
        {"q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "'Yesterday' (дирӯз) нишондиҳандаи замони гузашта (Past Simple) аст. Шакли гузаштаи 'go' -> 'went' мешавад."},
        {"q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "Барои муқоисаи ду шахс ба сифат суффикси '-er' илова карда мешавад."},
        {"q": "Have you ___ English before?", "options": ["study", "studied", "studying"], "correct": "studied", "rule": "Дар замони Present Perfect пас аз have/has шакли 3-юми феъл (V3) меояд."},
        {"q": "Listen! The baby ___.", "options": ["cries", "is crying", "cried"], "correct": "is crying", "rule": "Калимаи 'Listen!' нишон медиҳад, ки амал ҳозир рафта истодааст (Present Continuous)."},
        {"q": "There ___ some milk in the fridge.", "options": ["is", "are", "any"], "correct": "is", "rule": "Шир (milk) исми ҳисобнашаванда аст, бинобар ин дар шакли танҳо (is) меояд."},
        {"q": "I ___ a new movie last night.", "options": ["watched", "watch", "watching"], "correct": "watched", "rule": "'Last night' нишондиҳандаи замони гузашта (Past Simple) аст."},
        {"q": "This car is the ___ in the shop.", "options": ["most expensive", "more expensive", "expensive"], "correct": "most expensive", "rule": "Дараҷаи олии сифатҳои бисёрҳинҷо бо 'the most' сохта мешавад."},
        {"q": "She speaks English ___.", "options": ["well", "good", "bad"], "correct": "well", "rule": "Барои тасвири феъл (чи тавр гап мезанад?) зарфи 'well' истифода мешавад, на сифати 'good'."},
        {"q": "You ___ wash your hands before eating.", "options": ["should", "mustn't", "won't"], "correct": "should", "rule": "Барои додани маслиҳат феъли модалии 'should' (бояд, хуб мешуд) истифода мешавад."},
        {"q": "If it ___, we will stay at home.", "options": ["rains", "rain", "will rain"], "correct": "rains", "rule": "Дар ҷумлаҳои шартии намуди 1-ум, пас аз 'if' замони ҳозира (Present Simple) меояд."}
    ],
    "B1 (Intermediate)": [
        {"q": "If it rains, we ___ stay at home.", "options": ["will", "would", "shall"], "correct": "will", "rule": "First Conditional: Шарти ҳозира + Натиҷаи оянда (Will)."},
        {"q": "The book ___ written by him in 2024.", "options": ["was", "is", "were"], "correct": "was", "rule": "Passive Voice дар замони гузашта: исми танҳо + was + шакли 3-юми феъл."},
        {"q": "I look forward to ___ you.", "options": ["seeing", "see", "seen"], "correct": "seeing", "rule": "Ибораи 'look forward to' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"q": "I wish I ___ more time to study now.", "options": ["had", "have", "will have"], "correct": "had", "rule": "Пас аз 'I wish' барои орзуҳои замони ҳозира замони гузашта (Past Simple) истифода мешавад."},
        {"q": "By the time you arrive, the train ___ left.", "options": ["will have", "will", "has"], "correct": "will have", "rule": "Future Perfect барои амале, ки то вақти муайян дар оянда иҷро мешавад."},
        {"q": "He asked me where I ___.", "options": ["lived", "live", "did live"], "correct": "lived", "rule": "Қоидаи ҳамоҳангии замонҳо (Sequence of Tenses): агар аввал дар гузашта бошад, давомшавӣ ҳам ба гузашта мегузарад."},
        {"q": "You ___ better lock the door.", "options": ["had", "would", "should"], "correct": "had", "rule": "Ибораи 'had better' маънои 'хуб мешуд, ки...'-ро дорад ва пас аз он феъли оддӣ меояд."},
        {"q": "The man ___ stole the car was caught.", "options": ["who", "which", "whose"], "correct": "who", "rule": "Барои шахс ҷонишини нисбии 'who' истифода мешавад."},
        {"q": "I am used to ___ early in the morning.", "options": ["waking up", "wake up", "woke up"], "correct": "waking up", "rule": "Сохтори 'be used to' (одат кардан ба чизе) феъли бо суффикси '-ing'-ро талаб мекунад."},
        {"q": "Although it was cold, ___ she went out.", "options": ["❌ (нишон дода намешавад)", "but", "however"], "correct": "❌ (нишон дода намешавад)", "rule": "Дар англисӣ пас аз калимаи 'Although' (ҳарчанд ки) калимаи 'but' (аммо) истифода намешавад."}
    ],
    "B2 (Upper-Intermediate)": [
        {"q": "She avoids ___ sugar to lose weight.", "options": ["eating", "to eat", "eat"], "correct": "eating", "rule": "Феъли 'avoid' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"q": "You ___ look at the sun; it damages your eyes.", "options": ["mustn't", "don't have to", "needn't"], "correct": "mustn't", "rule": "'Mustn't' барои манъ кардани амали хатарнок ё қатъӣ истифода мешавад."},
        {"q": "I would have helped you if you ___ me.", "options": ["had asked", "asked", "have asked"], "correct": "had asked", "rule": "Third Conditional (ҷумлаи шартии намуди 3): would have + V3 + if + had + V3."},
        {"q": "The police ___ investigating the crime.", "options": ["are", "is", "was"], "correct": "are", "rule": "Калимаи 'Police' ҳамеша дар шакли ҷамъ ҳисоб мешавад ва феъли 'are'-ро мегирад."},
        {"q": "I'd rather you ___ anyone about this.", "options": ["didn't tell", "don't tell", "not to tell"], "correct": "didn't tell", "rule": "Пас аз сохтори 'I'd rather you' барои замони ҳозира феъл дар замони гузашта (Past Simple) меояд."},
        {"q": "Neither Myrat nor his friends ___ coming.", "options": ["are", "is", "was"], "correct": "are", "rule": "Дар сохтори 'Neither... nor...', феъл ба исми охирин (friends) ҳамоҳанг мешавад."},
        {"q": "He is said ___ a lot of money.", "options": ["to have", "having", "to having"], "correct": "to have", "rule": "Сохтори Complex Subject: He is said + to + феъли оддӣ."},
        {"q": "No sooner had he left ___ it started raining.", "options": ["than", "when", "then"], "correct": "than", "rule": "Сохтори 'No sooner' ҳамеша бо партикли 'than' истифода мешавад."},
        {"q": "I don't regret ___ the job.", "options": ["leaving", "to leave", "left"], "correct": "leaving", "rule": "Феъли 'regret' барои пушаймонӣ аз амали гузашта Герундий (-ing)-ро талаб мекунад."},
        {"q": "It's time we ___ home.", "options": ["went", "go", "to go"], "correct": "went", "rule": "Пас аз сохтори 'It's time' ҳамеша замони гузашта (Past Simple) истифода мешавад."}
    ],
    "C1 (Advanced)": [
        {"q": "Hardly ___ entered the room when the phone rang.", "options": ["had I", "I had", "did I"], "correct": "had I", "rule": "Инверсия: пас аз калимаи манфии 'Hardly' аввал феъли ёвар (had) ва баъд мубтадо (I) меояд."},
        {"q": "If I had studied harder, I ___ a degree now.", "options": ["would have", "would have had", "will have"], "correct": "would have", "rule": "Mixed Conditional (Шарти омехта): Шарти гузашта + Натиҷаи ҳозира."},
        {"q": "The CEO suggested ___ the meeting until next week.", "options": ["postponing", "to postpone", "postpone"], "correct": "postponing", "rule": "Феъли 'suggest' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"q": "She was completely taken ___ by his smooth words.", "options": ["in", "off", "away"], "correct": "in", "rule": "Феъли иборавии 'take in' маънои 'фиреб хӯрдан'-ро дорад."},
        {"q": "It is crucial that he ___ here on time.", "options": ["be", "is", "was"], "correct": "be", "rule": "Subjunctive Mood: пас аз 'It is crucial that' феъл дар шакли асосии худ (be) меояд."},
        {"q": "___ had I known the truth, I wouldn't have gone.", "options": ["❌ (Хат кашида шудааст)", "If", "Should"], "correct": "❌ (Хат кашида шудааст)", "rule": "Дар инверсияи шартӣ 'had' ба аввал меояд ва 'if' партофта мешавад."},
        {"q": "He is a person ___ integrity is unquestionable.", "options": ["whose", "who", "whom"], "correct": "whose", "rule": "'Whose' ҷонишини нисбии соҳибӣ (ки ҳалолмандиаш) мебошад."},
        {"q": "The project was cancelled owing ___ lack of funds.", "options": ["to", "for", "with"], "correct": "to", "rule": "Ибораи устувори 'owing to' маънои 'ба сабаби...'-ро дорад."},
        {"q": "Try ___ he might, he couldn't open the door.", "options": ["as", "though", "however"], "correct": "as", "rule": "Сохтори гузашт: Феъл + as + мубтадо + might (Ҳарчанд кӯшиш кард...)."},
        {"q": "Were it not ___ your help, I would fail.", "options": ["for", "with", "to"], "correct": "for", "rule": "Сохтори устувори шартии инверсиявӣ: 'Were it not for...' (Агар барои ёрии ту намешуд)."}
    ]
}

# БАЗАИ КОРБАРУН ДАР ХОТИРА
ALL_USERS = set()     # Барои ҳисоби ҳамаи корбарон
ACTIVE_USERS = set()  # Барои ҳисоби шахсони онлайн/актив
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
    
    # Илова ба базаи статистика
    ALL_USERS.add(user_id)
    ACTIVE_USERS.add(user_id)
    
    USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": [], "state": "CHOOSE_LEVEL"}
    
    welcome_text = (
        "👋 Welcome to the English Quiz Bot!\n\n"
        "👤 **Developer:** Abdurahim Sheraliev\n"
        "📚 **Маълумот:** Ин бот ба ту кӯмак мекунад, ки урувин (дараҷа)-и забони англисии худро бисанҷӣ.\n"
        "📝 Дар охири тест тамоми хатогиҳо бо забони тоҷикӣ фаҳмонда мешаванд!\n\n"
        "💡 Лутфан, дараҷаи худро интихоб кунед:"
    )
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("A1 (Beginner)"), KeyboardButton("A2 (Elementary)"))
    markup.add(KeyboardButton("B1 (Intermediate)"), KeyboardButton("B2 (Upper-Intermediate)"))
    markup.add(KeyboardButton("C1 (Advanced)"))
    
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# 📊 АДМИН-ПАНЕЛ БАРОИ АБДУРАҲИМ
@bot.message_handler(commands=['stat'])
def show_stat(message):
    total = len(ALL_USERS)
    online = len(ACTIVE_USERS)
    stat_text = (
        "📊 **Статистикаи Бот:**\n\n"
        "👥 Шумораи умумии корбарон: \n"
        f"└ **{total} нафар**\n\n"
        "🟢 Шахсони фаъол (Онлайн): \n"
        f"└ **{online} нафар**"
    )
    bot.send_message(message.from_user.id, stat_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    # Ҳар дафъае, ки кас паём менависад, фаъол ҳисоб мешавад
    ACTIVE_USERS.add(user_id)

    if user_id not in USER_DATA:
        start_quiz(message)
        return

    state = USER_DATA[user_id].get("state")

    if state == "CHOOSE_LEVEL":
        if text in QUIZ_DATA:
            USER_DATA[user_id]["level"] = text
            
            # 10 Саволро аз база гирифта омехта мекунем
            all_q = [item.copy() for item in QUIZ_DATA[text]]
            random.shuffle(all_q)
            
            USER_DATA[user_id]["questions"] = all_q[:10]  # Дақиқ 10 савол
            USER_DATA[user_id]["current_q"] = 0
            USER_DATA[user_id]["score"] = 0
            USER_DATA[user_id]["wrong_answers"] = []
            USER_DATA[user_id]["state"] = "QUIZ_RUNNING"
            
            bot.send_message(user_id, f"🏁 You have chosen {text}. The quiz has started! Total: 10 questions.", reply_markup=ReplyKeyboardRemove())
            send_question(user_id)
        else:
            bot.send_message(user_id, "Please, choose a level from the keyboard buttons.")

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
    text = f"❓ Question {current_q + 1} of {len(q_list)}:\n\n{question['q']}"
    
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
        result_text += "🛠 **Таҳлили хатогиҳо ва қоидаҳо (бо забони тоҷикӣ):**\n\n"
        for idx, w in enumerate(wrongs):
            result_text += (
                f"❌ Хатогии {idx+1}:\n"
                f"❓ Савол: {w['q']}\n"
                f"🔻 Интихоби шумо: {w['chosen']}\n"
                f"✅ Ҷавоби дуруст: {w['correct']}\n"
                f"💡 Қоида: {w['rule']}\n"
                f"-----------------------------\n"
            )
    else:
        result_text += "🎉 Awesome! You answered all questions correctly!"
            
    result_text += "\n🔄 Нависед /start барои аз нав оғоз кардан."
    USER_DATA[user_id]["state"] = "CHOOSE_LEVEL"
    bot.send_message(user_id, result_text, reply_markup=ReplyKeyboardRemove())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
