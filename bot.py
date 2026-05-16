import telebot

# Дар ин ҷо Тoken-и боти худро аз BotFather гузор
TOKEN = '8996159898:AAEFani_soW7FmDlf2Uvrga0ruJKWfN9r64'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салом! Боти ту дар Render бомуваффақият кор карда истодааст! 🚀")

if __name__ == "__main__":
    print("Бот ба кор даромад...")
    bot.infinity_polling()
