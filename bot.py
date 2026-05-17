import os
import threading
import random
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ⚠️ ТОКЕНИ ХУДРО ДАР БАЙНИ СИТАТАҲО БОДИҚҚАТ ГУЗОРЕД
TOKEN = '8996159898:AAEFani_soW7FmDlf2Uvrga0ruJKWfN9r64'

app = Flask(__name__)

@app.route('/')
def home():
    return "English Quiz Bot is running! 🚀"

# БАЗАИ САВОЛҲО БО ҲАМАИ ДАРАҶАҲО (A1, A2, B1, B2, C1)
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
    ],
    "B2 (Upper-Intermediate)": [
        {"q": "She avoids ___ sugar to lose weight.", "options": ["to eat", "eating", "eat"], "correct": "eating", "rule": "Феъли 'avoid' (худдорӣ кардан) пас аз худ ҳамеша Герундий (-ing)-ро талаб мекунад."},
        {"q": "You ___ look at the sun; it damages your eyes.", "options": ["mustn't", "don't have to", "needn't"], "correct": "mustn't", "rule": "Феъли модалии 'mustn't' барои манъ кардани амали хатарнок ё нораво истифода мешавад."},
        {"q": "I would have helped you if you ___ me.", "options": ["asked", "have asked", "had asked"], "rule": "Ин ҷумлаи шартии намуди сеюм (Third Conditional) аст: Натиҷаи гузашта (would have + V3) + Шарти гузашта (had + V3).", "correct": "had asked"}
    ],
    "C1 (Advanced)": [
        {"q": "Hardly ___ entered the room when the phone rang.", "options": ["I had", "had I", "I received"], "correct": "had I", "rule": "Ин сохтори инверсия (Inversion) аст. Баъд аз калимаҳои манфии 'Hardly' аввал феъли ёвар (had) ва баъд ҷонишин (I) меояд."},
        {"q": "If I had studied harder, I ___ a degree now.", "options": ["would have", "will have", "would have 3"], "correct": "would have", "rule": "Ин ҷумлаи шартии омехта (Mixed Conditional) аст: Шарти гузашта + Натиҷаи ҳозира."},
        {"q": "The CEO suggested ___ the meeting until next week.", "options": ["to postpone", "postponing", "postponed"], "correct": "postponing", "rule": "Феъли 'suggest' пас аз худ Герундий (-ing)-ро талаб мекунад."},
        {"q": "She was completely taken ___ by his smooth words.", "options": ["in", "off", "away"], "correct": "in", "rule": "Феъли иборавии 'take in' маънои 'фиреб хӯрдан'-ро дорад."},
        {"q": "It is crucial that he ___ here on time.", "options": ["is", "be", "was"], "correct": "be", "rule": "Ин сохтори Subjunctive Mood аст. Пас аз 'It is crucial that' феъл дар шакли асосии худ (be) меояд."}
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
        "📝 At the end, your mistakes will be explained in Tajik.\n\n"
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
        
        # Барои он ки 50 савол диҳад, мо саволҳоро зиёд мекунем (дубора такрор мекунем, агар кам бошанд)
        all_q = QUIZ_DATA[level].copy()
        random.shuffle(all_q)
        
        # Барои санҷиши устувор: Агар хоҳед дақиқ 50 савол шавад, рӯйхатро дароз мекунем
        extended_q = []
        while len(extended_q) < 50:
            random.shuffle(all_q)
            for item in all_q:
                extended_q.append(item.copy())
                if len(extended_q) == 50:
                    break
                    
        USER_DATA[user_id]["questions"] = extended_q
        USER_DATA[user_id]["current_q"] = 0
        USER_DATA[user_id]["score"] = 0
        USER_DATA[user_id]["wrong_answers"] = []
        
        # Навсозии матни тугмаҳо бо кафолати ирсоли савол
        await query.message.reply_text(f"🏁 You have chosen **{level}**. The quiz has started with 50 questions!")
        await send_question(query, user_id)

    elif data.startswith("ans:"):
        _, ans_idx, correct_str = data.split(":")
        current_q_idx = USER_DATA[user_id]["current_q"]
        q_list = USER_DATA[user_id]["questions"]
        
        if current_q_idx < len(q_list):
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

async def send_question(query, user_id: int):
    current_q = USER_DATA[user_id]["current_q"]
    q_list = USER_DATA[user_id]["questions"]

    if current_q >= len(q_list) or current_q >= 50:
        await show_results(query, user_id)
        return

    question = q_list[current_q]
    text = f"❓ **Question {current_q + 1}/50:**\n\n{question['q']}"
    
    keyboard = []
    for idx, opt in enumerate(question["options"]):
        is_correct = "yes" if opt == question["correct"] else "no"
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"ans:{idx}:{is_correct}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Истифодаи бевоситаи query.message барои кафолати 100% баромадани савол
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_results(query, user_id: int):
    score = USER_DATA[user_id]["score"]
    wrongs = USER_DATA[user_id]["wrong_answers"]
    
    result_text = f"🏁 **The quiz is over!**\n\n📊 Your score: **{score} out of 50**\n\n"
    
    if wrongs:
        result_text += "🛠 **Таҳлили хатогиҳо ва қоидаҳо (бо забони тоҷикӣ):**\n\n"
        # Танҳо 15 хатогии аввалро нишон медиҳем, то паём дар Telegram хеле дароз ва хато нашавад
        for idx, w in enumerate(wrongs[:15]):
            result_text += (
                f"❌ *Хатогии {idx+1}:*\n"
                f"❓ Савол: `{w['q']}`\n"
                f"🔻 Интихоби шумо: {w['chosen']}\n"
                f"✅ Ҷавоби дуруст: *{w['correct']}*\n"
                f"💡 **Қоида:** {w['rule']}\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            )
        if len(wrongs) > 15:
            result_text += f"➕ Ва боз {len(wrongs) - 15} хатогии дигар..."
    else:
        result_text += "🎉 Awesome! You answered all 50 questions correctly!"

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
