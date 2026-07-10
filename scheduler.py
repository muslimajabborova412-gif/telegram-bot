from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import ContextTypes
from database import get_all_users
from config import CHANNEL_USERNAME

async def send_daily_test(context: ContextTypes.DEFAULT_TYPE):
    """Функсия барои фиристодани тести автоматӣ ба ҳамаи корбарон"""
    users = get_all_users()
    
    # Саволи намунавӣ барои тест (Telegram Poll)
    question = "By next year, we _______ here for ten years."
    options = ["will live", "will be living", "will have been living"]
    correct_option_id = 2 # Варианти 3-юм дуруст аст (индекс аз 0 сар мешавад)
    
    for user_id in users:
        try:
            # Фиристодани тест дар намуди Викторина (Quiz)
            await context.bot.send_poll(
                chat_id=user_id,
                question=question,
                options=options,
                type="quiz",
                correct_option_id=correct_option_id,
                explanation="Дарси Future Perfect Continuous-ро ба ёд оред! 😉",
                explanation_parse_mode="Markdown"
            )
            
            # Рекламаи канал дар зери тест
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📚 Тестҳои бештар ва китобҳо дар канали мо:\n👉 {CHANNEL_USERNAME}"
            )
        except Exception as e:
            print(f"Хатогӣ ҳангоми фиристодан ба {user_id}: {e}")

def start_scheduler(application):
    """Ба кор андохтани таймер барои автопостинг"""
    scheduler = BackgroundScheduler(timezone="Asia/Dushanbe")
    
    # Ҳар рӯз соати 09:00-и субҳ тест мефиристад
    scheduler.add_job(
        lambda: application.job_queue.run_once(send_daily_test, when=0),
        'cron',
        hour=9,
        minute=0
    )
    
    scheduler.start()
