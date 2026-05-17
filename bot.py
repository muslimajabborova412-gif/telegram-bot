import os
import random
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8996159898:AAH4t65DElUHgVtQrx5Ck0j8LyBVuWqPmwQ'
WEBHOOK_URL = 'https://telegram-bot-quiz-3cqc.onrender.com'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

QUIZ_DATA = {
    "A1 (Beginner)": [
        {"q": "I ___ from Tajikistan.", "options": ["am", "is", "are"], "correct": "am", "rule": "With the pronoun 'I', we always use the verb to-be 'am'."},
        {"q": "She ___ a book every day.", "options": ["read", "reads", "reading"], "correct": "reads", "rule": "In Present Simple, we add '-s' or '-es' to the verb for He/She/It."},
        {"q": "Where ___ you live?", "options": ["do", "does", "is"], "correct": "do", "rule": "We use the auxiliary verb 'do' to form questions with 'you'."},
        {"q": "They ___ have a car.", "options": ["don't", "doesn't", "not"], "correct": "don't", "rule": "The negative form for 'They' in Present Simple is 'don't'."},
        {"q": "He ___ football on Sundays.", "options": ["plays", "play", "playing"], "correct": "plays", "rule": "For the singular third-person pronoun 'He', the verb takes an '-s'."},
        {"q": "This is ___ apple.", "options": ["an", "a", "the"], "correct": "an", "rule": "We use the article 'an' before words that start with a vowel sound."},
        {"q": "We ___ happy today.", "options": ["are", "am", "is"], "correct": "are", "rule": "We use the plural verb to-be 'are' with 'We/They/You'."},
        {"q": "What is ___ name?", "options": ["your", "you", "yours"], "correct": "your", "rule": "The possessive adjective 'your' is used before a noun."},
        {"q": "Look at ___ birds in the sky over there.", "options": ["those", "these", "this"], "correct": "those", "rule": "'Those' points to plural objects that are far away."},
        {"q": "I have ___ brothers.", "options": ["two", "to", "too"], "correct": "two", "rule": "'Two' is the correct spelling for the number 2."}
    ],
    "A2 (Elementary)": [
        {"q": "Yesterday I ___ to the park.", "options": ["go", "went", "gone"], "correct": "went", "rule": "'Yesterday' indicates Past Simple. The past form of 'go' is 'went'."},
        {"q": "He is ___ than his brother.", "options": ["tall", "taller", "tallest"], "correct": "taller", "rule": "We add '-er' to short adjectives for comparative forms."},
        {"q": "Have you ___ English before?", "options": ["study", "studied", "studying"], "correct": "studied", "rule": "In Present Perfect, we use 'have/has' followed by the past participle (V3)."},
        {"q": "Listen! The baby ___.", "options": ["cries", "is crying", "cried"], "correct": "is crying", "rule": "The word 'Listen!' shows that the action is happening right now (Present Continuous)."},
        {"q": "There ___ some milk in the fridge.", "options": ["is", "are", "any"], "correct": "is", "rule": "'Milk' is an uncountable noun, so it takes the singular verb 'is'."},
        {"q": "I ___ a new movie last night.", "options": ["watched", "watch", "watching"], "correct": "watched", "rule": "'Last night' is a clear time marker for Past Simple."},
        {"q": "This car is the ___ in the shop.", "options": ["most expensive", "more expensive", "expensive"], "correct": "most expensive", "rule": "The superlative of long adjectives is formed using 'the most'."},
        {"q": "She speaks English ___.", "options": ["well", "good", "bad"], "correct": "well", "rule": "We use the adverb 'well' to describe how someone performs an action (speaks)."},
        {"q": "You ___ wash your hands before eating.", "options": ["should", "mustn't", "won't"], "correct": "should", "rule": "The modal verb 'should' is used to give advice or suggestions."},
        {"q": "If it ___, we will stay at home.", "options": ["rains", "rain", "will rain"], "correct": "rains", "rule": "In First Conditional sentences, we use Present Simple after 'if'."}
    ],
    "B1 (Intermediate)": [
        {"q": "If it rains, we ___ stay at home.", "options": ["will", "would", "shall"], "correct": "will", "rule": "First Conditional: Present condition + Future result (will + verb)."},
        {"q": "The book ___ written by him in 2024.", "options": ["was", "is", "were"], "correct": "was", "rule": "Passive Voice in the past: singular noun + was + V3."},
        {"q": "I look forward to ___ you.", "options": ["seeing", "see", "seen"], "correct": "seeing", "rule": "The phrase 'look forward to' must be followed by a gerund (-ing form)."},
        {"q": "I wish I ___ more time to study now.", "options": ["had", "have", "will have"], "correct": "had", "rule": "After 'I wish', we use Past Simple to express present regrets or desires."},
        {"q": "By the time you arrive, the train ___ left.", "options": ["will have", "will", "has"], "correct": "will have", "rule": "Future Perfect describes an action that will be completed before a specific time in the future."},
        {"q": "He asked me where I ___.", "options": ["lived", "live", "did live"], "correct": "lived", "rule": "Sequence of tenses: if the reporting verb is in the past, the reported speech moves to the past."},
        {"q": "You ___ better lock the door.", "options": ["had", "would", "should"], "correct": "had", "rule": "The idiom 'had better' means 'should' and is followed by a base verb."},
        {"q": "The man ___ stole the car was caught.", "options": ["who", "which", "whose"], "correct": "who", "rule": "We use the relative pronoun 'who' for people."},
        {"q": "I am used to ___ early in the morning.", "options": ["waking up", "wake up", "woke up"], "correct": "waking up", "rule": "The structure 'be used to' requires a gerund (-ing) because 'to' is a preposition here."},
        {"q": "Although it was cold, ___ she went out.", "options": ["❌ (No word)", "but", "however"], "correct": "❌ (No word)", "rule": "We do not use 'but' in the main clause if the sentence starts with 'Although'."}
    ],
    "B2 (Upper-Intermediate)": [
        {"q": "She avoids ___ sugar to lose weight.", "options": ["eating", "to eat", "eat"], "correct": "eating", "rule": "The verb 'avoid' is always followed by a gerund (-ing)."},
        {"q": "You ___ look at the sun; it damages your eyes.", "options": ["mustn't", "don't have to", "needn't"], "correct": "mustn't", "rule": "'Mustn't' is used to express strong prohibition or safety warnings."},
        {"q": "I would have helped you if you ___ me.", "options": ["had asked", "asked", "have asked"], "correct": "had asked", "rule": "Third Conditional: would have + V3 + if + Past Perfect (had + V3)."},
        {"q": "The police ___ investigating the crime.", "options": ["are", "is", "was"], "correct": "are", "rule": "The noun 'police' is a collective noun that is always treated as plural."},
        {"q": "I'd rather you ___ anyone about this.", "options": ["didn't tell", "don't tell", "not to tell"], "correct": "didn't tell", "rule": "After 'I'd rather someone', we use Past Simple to talk about the present preference."},
        {"q": "Neither Myrat nor his friends ___ coming.", "options": ["are", "is", "was"], "correct": "are", "rule": "With 'neither... nor...', the verb agrees with the closest subject (friends)."},
        {"q": "He is said ___ a lot of money.", "options": ["to have", "having", "to having"], "correct": "to have", "rule": "Complex Subject: Subject + passive verb + to-infinitive."},
        {"q": "No sooner had he left ___ it started raining.", "options": ["than", "when", "then"], "correct": "than", "rule": "The correlative structure 'No sooner' always links with 'than'."},
        {"q": "I don't regret ___ the job.", "options": ["leaving", "to leave", "left"], "correct": "leaving", "rule": "The verb 'regret' takes a gerund (-ing) when talking about past decisions."},
        {"q": "It's time we ___ home.", "options": ["went", "go", "to go"], "correct": "went", "rule": "The structure 'It's time we...' requires the Past Simple tense."}
    ],
    "C1 (Advanced)": [
        {"q": "Hardly ___ entered the room when the phone rang.", "options": ["had I", "I had", "did I"], "correct": "had I", "rule": "Inversion: when starting with negative adverbs like 'Hardly', the auxiliary verb comes before the subject."},
        {"q": "If I had studied harder, I ___ a degree now.", "options": ["would have", "would have had", "will have"], "correct": "would have", "rule": "Mixed Conditional: Past hypothetical condition + Present result."},
        {"q": "The CEO suggested ___ the meeting until next week.", "options": ["postponing", "to postpone", "postpone"], "correct": "postponing", "rule": "The verb 'suggest' takes a gerund (-ing) when there is no direct object pronoun."},
        {"q": "She was completely taken ___ by his smooth words.", "options": ["in", "off", "away"], "correct": "in", "rule": "The phrasal verb 'take in' means to deceive or trick someone."},
        {"q": "It is crucial that he ___ here on time.", "options": ["be", "is", "was"], "correct": "be", "rule": "Subjunctive Mood: after expressions of urgency/importance, the base form (be) is used."},
        {"q": "___ had I known the truth, I wouldn't have gone.", "options": ["❌ (No word)", "If", "Should"], "correct": "❌ (No word)", "rule": "In inverted conditional sentences, 'had' replaces 'if', so 'if' is omitted."},
        {"q": "He is a person ___ integrity is unquestionable.", "options": ["whose", "who", "whom"], "correct": "whose", "rule": "'Whose' is a relative possessive pronoun indicating possession by a person."},
        {"q": "The project was cancelled owing ___ lack of funds.", "options": ["to", "for", "with"], "correct": "to", "rule": "'Owing to' is a fixed prepositional phrase meaning 'because of'."},
        {"q": "Try ___ he might, he couldn't open the door.", "options": ["as", "though", "however"], "correct": "as", "rule": "Concessive structure: Verb + as + subject + modal (meaning 'Even though he tried...')."},
        {"q": "Were it not ___ your help, I would fail.", "options": ["for", "with", "to"], "correct": "for", "rule": "Inverted second conditional idiom: 'Were it not for...' means 'If it weren't for...'"}
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
    status = bot.set_webhook(url=WEBHOOK_URL + '/' + TOKEN)
    return f"Webhook status: {status} 🚀"

@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_id = message.from_user.id
    ALL_USERS.add(user_id)
    ACTIVE_USERS.add(user_id)
    
    welcome_text = (
        "👋 **Welcome to the English_TestBot!**\n\n"
        "👤 **Developer:** Abdurahim Sheraliev\n"
        "📚 **Information:** This bot helps you test your English proficiency levels from A1 to C1.\n\n"
        "💡 Please, select your level to begin:"
    )
    
    markup = InlineKeyboardMarkup()
    for lvl in QUIZ_DATA.keys():
        markup.add(InlineKeyboardButton(lvl, callback_data=f"start_lvl:{lvl}"))
        
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['stat'])
def show_stat(message):
    bot.send_message(
        message.from_user.id,
        f"📊 **Statistics:**\n\n👥 Total Users: **{len(ALL_USERS)}**\n🟢 Active Online Users: **{len(ACTIVE_USERS)}**",
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = call.data
    ACTIVE_USERS.add(user_id)

    if data.startswith("start_lvl:"):
        level = data.split(":")[1]
        
        all_q = [item.copy() for item in QUIZ_DATA[level]]
        random.shuffle(all_q)
        
        USER_DATA[user_id] = {
            "level": level,
            "questions": all_q[:10],
            "current_q": 0,
            "score": 0,
            "wrong_answers": []
        }
        
        bot.send_message(user_id, f"🏁 **You have chosen {level}. The quiz has started!**", parse_mode="Markdown")
        send_question(user_id)

    elif data.startswith("ans:"):
        _, is_correct, ans_idx = data.split(":")
        
        if user_id in USER_DATA:
            current_q_idx = USER_DATA[user_id]["current_q"]
            q_list = USER_DATA[user_id]["questions"]
            
            if current_q_idx < len(q_list):
                current_question = q_list[current_q_idx]
                chosen_option = current_question["options"][int(ans_idx)]
                
                updated_text = f"❓ **Question {current_q_idx + 1}/{len(q_list)}:**\n`{current_question['q']}`\n\n📥 *Your choice:* {chosen_option}"
                bot.edit_message_text(updated_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, parse_mode="Markdown")
                
                if is_correct == "1":
                    USER_DATA[user_id]["score"] += 1
                    bot.answer_callback_query(call.id, "✅ Correct!")
                else:
                    USER_DATA[user_id]["wrong_answers"].append({
                        "q": current_question["q"],
                        "chosen": chosen_option,
                        "correct": current_question["correct"],
                        "rule": current_question["rule"]
                    })
                    bot.answer_callback_query(call.id, "❌ Incorrect!")
                
                USER_DATA[user_id]["current_q"] += 1
                send_question(user_id)

def send_question(user_id):
    current_q = USER_DATA[user_id]["current_q"]
    q_list = USER_DATA[user_id]["questions"]

    if current_q >= len(q_list):
        show_results(user_id)
        return

    question = q_list[current_q]
    text = f"❓ **Question {current_q + 1}/{len(q_list)}:**\n\n`{question['q']}`"
    
    markup = InlineKeyboardMarkup()
    for idx, opt in enumerate(question["options"]):
        is_correct = "1" if opt == question["correct"] else "0"
        markup.add(InlineKeyboardButton(opt, callback_data=f"ans:{is_correct}:{idx}"))
        
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

def show_results(user_id):
    score = USER_DATA[user_id]["score"]
    wrongs = USER_DATA[user_id]["wrong_answers"]
    total = len(USER_DATA[user_id]["questions"])
    
    percentage = int((score / total) * 100) if total > 0 else 0
    
    result_text = (
        f"🏁 **The quiz is over!**\n\n"
        f"📊 Your score: **{score} out of {total}**\n"
        f"🎯 Your proficiency level: **{percentage}%**\n\n"
    )
    
    if wrongs:
        result_text += "🛠 **Mistakes Analysis & Explanations:**\n\n"
        for idx, w in enumerate(wrongs):
            result_text += (
                f"❌ *Mistake {idx+1}:*\n"
                f"❓ Question: `{w['q']}`\n"
                f"🔻 Your answer: {w['chosen']}\n"
                f"✅ Correct answer: *{w['correct']}*\n"
                f"💡 **Grammar Rule:** {w['rule']}\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            )
    else:
        result_text += "🎉 **Awesome! Perfect score! 100% correct answers!**"

    result_text += "\n🔄 Type /start to take the quiz again."
    bot.send_message(user_id, result_text, parse_mode="Markdown")
