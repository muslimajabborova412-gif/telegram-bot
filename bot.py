import os
import telebot
from telebot import types
import random

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))

# Функция барои хондани калимаҳо
def get_words():
    with open("words.txt", "r", encoding="utf-8") as f:
        return [line.strip().split(';') for line in f if line.strip()]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📋 Омӯзиш", callback_data="learn"),
               types.InlineKeyboardButton("❓ Тест", callback_data="quiz"))
    bot.reply_to(message, "Салом! Якеро интихоб кунед:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "learn":
        # Нишон додани тугмаҳои Юнитҳо барои омӯзиш
        markup = types.InlineKeyboardMarkup(row_width=3)
        buttons = [types.InlineKeyboardButton(f"U{i}", callback_data=f"u_{i}") for i in range(1, 31)]
        markup.add(*buttons)
        bot.edit_message_text("Кадом Юнит-ро омӯхтан мехоҳед?", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data.startswith("u_"):
        unit_num = call.data.split("_")[1]
        words = get_words()
        text = f"📚 **Юнити {unit_num}**:\n" + "\n".join([f"🔹 {w[1]} — {w[2]}" for w in words if w[0] == unit_num])
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

    elif call.data == "quiz":
        # Тест: гирифтани калимаи тасодуфӣ
        words = get_words()
        word = random.choice(words)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(word[2], callback_data=f"ans_{word[1]}")) # Ин ҷо логикаи санҷиш илова мешавад
        bot.send_message(call.message.chat.id, f"Калимаи '{word[1]}' чӣ маъно дорад?", reply_markup=markup)

# Ин код заминаи тест аст.
