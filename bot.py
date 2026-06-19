import os
from flask import Flask
from telegram import Bot

TOKEN = "8201016798:AAEwG4rrqu-9o1H-wOdVzSr6WPZal_6_7N0"
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот кор мекунад!"

if __name__ == '__main__':
    # Render порту 10000-ро талаб мекунад
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
