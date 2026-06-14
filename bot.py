import os
import telebot
from telebot import types

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # Тугмаҳо барои интихоби корбар
    markup.add(types.InlineKeyboardButton("📚 Омӯзиш (Юнитҳо)", callback_data="learn"))
    markup.add(types.InlineKeyboardButton("❓ Тест", callback_data="quiz"))
    bot.reply_to(message, "Салом! Чӣ кор кардан мехоҳед?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "learn":
        markup = types.InlineKeyboardMarkup(row_width=3)
        # Тугмаҳо барои 30 Юнит
        buttons = [types.InlineKeyboardButton(f"U{i}", callback_data=f"unit_{i}") for i in range(1, 31)]
        markup.add(*buttons)
        bot.edit_message_text("Кадом Юнит-ро интихоб мекунед?", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data.startswith("unit_"):
        unit_num = call.data.split("_")[1]
        try:
            with open("words.txt", "r", encoding="utf-8") as f:
                lines = [line.strip().split(';') for line in f if line.startswith(f"{unit_num};")]
            
            if not lines:
                bot.answer_callback_query(call.id, "Калимаҳо ёфт нашуданд!")
                return
            
            text = f"📚 **Юнити {unit_num}**:\n\n" + "\n".join([f"🔹 *{w[1]}* — {w[2]}" for w in lines])
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        except:
            bot.answer_callback_query(call.id, "Хатогӣ рух дод!")

    elif call.data == "quiz":
        bot.send_message(call.message.chat.id, "Режими тест дар оянда илова мешавад!")

# Ин қисм барои Flask (барои он ки дар Render хомӯш нашавад)
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

if __name__ == '__main__':
    import threading
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
