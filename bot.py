import os
import threading
import random
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ⚠️ ТОКЕНИ ХУДРО ДАР БАЙНИ СИТАТАҲО ГУЗОР
TOKEN = '8996159898:AAEFani_soW7FmDlf2Uvrga0ruJKWfN9r64'

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! 🚀"

# БАЗАИ САВОЛҲО (Саволҳо зиёд карда шуданд ва функсияи санҷиш ислоҳ шуд)
QUIZ_DATA = {
    "A1 (Beginner)": [
        {"q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "Бо ҷонишини 'I' (ман) ҳамеша феъли то-be 'am' истифода мешавад."},
        {"q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "Дар замони Present Simple барои шахси сеюми танҳо (He, She, It) ба охири феъл суффикси '-s' ё '-es' илова мешавад."},
        {"q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "Барои сохтани ҷумлаи саволӣ дар замони Present Simple бо ҷонишини 'you' феъли ёвари 'do' истифода мешавад."},
        {"q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "Инкори ҷумла дар замони Present Simple барои шакли ҷамъ (They) бо ёрии 'don't' сохта мешавад."},
        {"q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "Дар Present Simple барои He/She/It ба феъл '-s' илова мешавад."}
    ],
    "A2 (Elementary)": [
        {"q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "Калимаи 'Yesterday' (дирӯз) нишон медиҳад, ки ҷумла дар замони гузаштаи оддӣ (Past Simple) аст. Феъли нодурусти 'go' дар замони гузашта 'went' мешавад."},
        {"q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "Барои муқоисаи ду шахс ё ашё (Comparative degree) ба сифатҳои кӯтоҳ суффикси '-er' илова карда мешавад."},
        {"q": "Have you ___ English before?", "options": ["study", "studied", "studying"], "correct": "studied", "rule": "Дар замони Present Perfect пас аз 'have/has' ҳамеша шакли сеюми феъл (V3) ё феъли бо суффикси '-ed' истифода мешавад."},
        {"q": "Listen! The baby ___.", "options": ["cries", "is crying", "cried"], "correct": "is crying", "rule": "Калимаи 'Listen!' (Гӯш кун!) нишон медиҳад, ки амал дар ҳамин сонияи гап задан рафта истодааст (Present Continuous: am/is/are + V-ing)."},
        {"q": "There ___ some milk in the fridge.", "options": ["is", "are", "any"], "correct": "is", "rule": "Ибораи 'milk' (шир) исми ҳисобнашаванда аст, бинобар ин бо он феъли шакли танҳо (is) истифода мешавад."}
    ],
    "B1 (Intermediate)": [
        {"q": "If it rains, we ___ stay at home.", "options": ["will", "would", "shall"], "correct": "will", "rule": "Ин ҷумлаи шартии намуди якум (First Conditional) аст: Шарти ҳозира (Present) + Натиҷаи оянда (Will)."},
        {"q": "The book ___ written by him in 2024.", "options": ["is", "was", "were"], "correct": "was", "rule": "Ин ҷумла дар замони гузаштаи маҷҳул (Passive Voice) аст. Шакли танҳо (The book) + was + шакли 3-юми феъл (written)."},
        {"q": "I look forward to ___ you.", "options": ["see", "seeing", "seen"], "correct": "seeing", "rule": "Ибораи 'look forward to' (бесаброна интизор будан) ҳамеша пас аз худ феъли бо суффикси '-ing' (Gerund)-ро талаб мекунад."},
        {"q": "I wish I ___ more time to study.", "options": ["have", "had", "will have"], "correct": "had", "rule": "Барои ифодаи пушаймонӣ ё орзу дар бораи замони ҳозира пас аз сохтори 'I wish' замони гузашта (Past Simple) истифода мешавад."},
        {"q": "By the time you arrive, the train ___ left.", "options": ["will", "will have", "has"], "correct": "will have", "rule": "Ин замони Future Perfect аст. Амале, ки то як вақти муайян дар оянда иҷро шуда ба охир мерасад (will have + V3)."}
    ]
}

USER_DATA = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": []}
    
    welcome_text = (
        "👋 Welcome to the English Quiz Bot!\n\n"
        "👤 **Developer:** Abdurahim Sheraliev\n"
        "📚 This bot will help you test your English language levels.\n"
        "📝 The quiz consists of questions. At the end, your mistakes will be explained in Tajik.\n\n"
        "💡 Please, choose your level:"
    )
    
    keyboard = [[InlineKeyboardButton(lvl, callback_data=f"set_lvl:{lvl}")] for lvl in QUIZ_DATA.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"score": 0, "current_q": 0, "level": "", "questions": [], "wrong_answers": []}

    if data.startswith("set_lvl:"):
        level = data.split(":")[1]
        USER_DATA[user_id]["level"] = level
        
        all_q = QUIZ_DATA[level].copy()
        random.shuffle(all_q)
        
        # Дигар хатогӣ намешавад: агар саволҳо аз 10 кам бошанд, ҳамаашро мегирад
        USER_DATA[user_id]["questions"] = all_q
        USER_DATA[user_id]["current_q"] = 0
        USER_DATA[user_id]["score"] = 0
        USER_DATA[user_id]["wrong_answers"] = []
        
        await query.message.reply_text(f"🏁 You have chosen **{level}**. The quiz has started!")
        await send_question(query, user_id)

    elif data.startswith("ans:"):
        _, ans_idx, correct_str = data.split(":")
        current_q_idx = USER_DATA[user_id]["current_q"]
        q_list = USER_DATA[user_id]["questions"]
        
        current_question = q_list[current_q_idx]
        chosen_option = current_question["options"][int(ans_idx)]
        
        if correct_str == "yes":
            USER_DATA[user_id]["score"] += 1
        else:
            USER_DATA[user_id]["wrong_answers"].append({
                "q": current_question["q"],
                "chosen": chosen_option,
                "correct": current_question["correct"],
                "rule": current_question["rule"]
            })
            
        USER_DATA[user_id]["current_q"] += 1
        await send_question(query, user_id)

async def send_question(query, user_id):
    current_q = USER_DATA[user_id]["current_q"]
    q_list = USER_DATA[user_id]["questions"]

    if current_q >= len(q_list):
        await show_results(query, user_id)
        return

    question = q_list[current_q]
    text = f"❓ **Question {current_q + 1}/{len(q_list)}:**\n\n{question['q']}"
    
    keyboard = []
    for idx, opt in enumerate(question["options"]):
        is_correct = "yes" if opt == question["correct"] else "no"
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"ans:{idx}:{is_correct}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_results(query, user_id):
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
        result_text += "🎉 Awesome! You answered all questions correctly!"

    result_text += "\n🔄 Press /start to try again."
    await query.message.reply_text(result_text, parse_mode="Markdown")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def main() -> None:
    threading.Thread(target=run_flask, daemon=True).start()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print("Bot started successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
