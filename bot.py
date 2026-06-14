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

# Базаи калимаҳо бо мисолҳо аз рӯи китоби ту
DATA_BASE = {
    "1": [
        {"word": "Agree", "translation": "Рози шудан", "example": "I agree with your opinion."},
        {"word": "Alcohol", "translation": "Алкогол (нӯшокии спиртӣ)", "example": "Alcohol is bad for health."},
        {"word": "Arrive", "translation": "Омадан, расидан", "example": "The train will arrive at 5 PM."},
        {"word": "August", "translation": "Август", "example": "August is the eighth month of the year."},
        {"word": "Boat", "translation": "Қаиқ, киштӣ", "example": "We rode a small boat on the lake."},
        {"word": "Breakfast", "translation": "Нонушта", "example": "I had a healthy breakfast this morning."},
        {"word": "Camera", "translation": "Camera", "example": "He took a picture with his new camera."},
        {"word": "Capital", "translation": "Пойтахт", "example": "Dushanbe is the capital of Tajikistan."},
        {"word": "Catch", "translation": "Доштан, қапидан", "example": "Did you catch the ball?"},
        {"word": "Duck", "translation": "Мурғобӣ", "example": "The duck is swimming in the pond."},
        {"word": "Enjoy", "translation": "Ҳаловат бурдан", "example": "We enjoyed our time at the beach."},
        {"word": "Invite", "translation": "Даъват кардан", "example": "They invited me to the party."},
        {"word": "Love", "translation": "Дӯст доштан", "example": "I love my family very much."},
        {"word": "Month", "translation": "Моҳ", "example": "January is the first month of the year."},
        {"word": "Travel", "translation": "Саёҳат кардан", "example": "I want to travel to Japan."},
        {"word": "Typical", "translation": "Одатӣ, маъмулӣ", "example": "It was a typical cold winter day."},
        {"word": "Visit", "translation": "Хабар гирифтан", "example": "I will visit my grandparents tomorrow."},
        {"word": "Weather", "translation": "Обу ҳаво", "example": "The weather is very hot today."},
        {"word": "Week", "translation": "Ҳафта", "example": "There are seven days in a week."},
        {"word": "Wine", "translation": "Шароб (вино)", "example": "Wine is made from grapes."}
    ],
    "2": [
        {"word": "Adventure", "translation": "Саргузашт", "example": "They went on a wild adventure in the jungle."},
        {"word": "Approach", "translation": "Наздик шудан", "example": "The boy approached the barking dog carefully."},
        {"word": "Carefully", "translation": "Боэҳтиёт", "example": "Please carry the glasses carefully."},
        {"word": "Chemical", "translation": "Моддаи химиявӣ", "example": "The scientist mixed the chemicals together."},
        {"word": "Create", "translation": "Сохтан, эҷод кардан", "example": "She created a beautiful painting."},
        {"word": "Evil", "translation": "Бадӣ, ҷоҳил", "example": "The evil witch cursed the castle."},
        {"word": "Experiment", "translation": "Таҷриба, озмоиш", "example": "We did an experiment in science class."},
        {"word": "Kill", "translation": "Куштан", "example": "The hunter killed a deer for food."},
        {"word": "Laboratory", "translation": "Лаборатория", "example": "They work in a high-tech laboratory."},
        {"word": "Laugh", "translation": "Ханда", "example": "His funny joke made everyone laugh."}
    ],
    "3": [
        {"word": "Alien", "translation": "Мавҷудоти бегона", "example": "The alien arrived in a flying saucer."},
        {"word": "Among", "translation": "Дар байни", "example": "There is a red apple among the green ones."},
        {"word": "Chart", "translation": "Ҷадвал, диаграмма", "example": "We used a chart to track our sales progress."},
        {"word": "Cloud", "translation": "Абр", "example": "Look at that white cloud in the blue sky."},
        {"word": "Describe", "translation": "Тавсиф кардан", "example": "Can you describe what the man looked like?"},
        {"word": "Fail", "translation": "Ноком шудан", "example": "If you do not study, you might fail the test."},
        {"word": "Grade", "translation": "Баҳо, синф", "example": "He got a good grade on his English exam."},
        {"word": "Library", "translation": "Китобхона", "example": "I go to the library to study quietly."},
        {"word": "Planet", "translation": "Сайёра", "example": "Earth is the third planet from the sun."},
        {"word": "Solve", "translation": "Ҳал кардан", "example": "She managed to solve the hard math problem."}
    ]
}

user_states = {}

# Тугмаҳои инлайнии Юнитҳо
def get_inline_units_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(1, 31):
        buttons.append(types.InlineKeyboardButton(f"Unit {i}", callback_data=f"list_unit_{i}"))
    markup.add(*buttons)
    return markup

# Тугмаи оғози тест
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
    # Истифодаи ReplyKeyboardRemove барои он ки ягон тугмаи кӯҳна дар поён намонад
    bot.send_message(message.chat.id, welcome_msg, reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "Интихоби Юнит 👇", reply_markup=get_inline_units_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("list_unit_"):
        unit_number = data.split("_")[2]
        
        if unit_number in DATA_BASE and DATA_BASE[unit_number]:
            response = f"📖 **Рӯйхати луғатҳои Unit {unit_number} (Бо мисолҳо):**\n\n"
            for i, item in enumerate(DATA_BASE[unit_number], 1):
                response += f"{i}. 🔤 **{item['word']}** = 🇹🇯 {item['translation']}\n📝 _Мисол:_ {item['example']}\n\n"
            
            bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=get_inline_quiz_keyboard(unit_number))
        else:
            bot.send_message(chat_id, f"ℹ️ Калимаҳо бо мисолҳояшон барои **Unit {unit_number}** ба наздикӣ илова карда мешаванд!", reply_markup=get_inline_units_keyboard())
        
        bot.answer_callback_query(call.id)

    elif data == "back_to_units":
        bot.send_message(chat_id, "📚 **Кадом Юнитро хондан мехоҳӣ?**", reply_markup=get_inline_units_keyboard())
        bot.answer_callback_query(call.id)

    elif data.startswith("start_quiz_"):
        unit_number = data.split("_")[2]
        unit_words = DATA_BASE.get(unit_number, [])
        
        if not unit_words:
            bot.send_message(chat_id, f"❌ Дар Unit {unit_number} калима барои тест ёфт нашуд.")
            bot.answer_callback_query(call.id)
            return

        shuffled_questions = random.sample(unit_words, min(10, len(unit_words)))
        
        all_words_pool = []
        for uw in DATA_BASE.values():
            all_words_pool.extend(uw)

        user_states[chat_id] = {
            "quiz_list": shuffled_questions,
            "quiz_index": 0,
            "score": 0,
            "last_poll_id": None,
            "correct_answer": "",
            "all_pool": all_words_pool
        }
        
        bot.send_message(chat_id, f"🚀 Тести махсус аз **Юнит {unit_number}** оғоз шуд (10 Савол)!")
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
