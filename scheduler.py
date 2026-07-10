import datetime
from telegram.ext import ContextTypes
from database import get_all_users
from config import CHANNEL_USERNAME

async def send_daily_test(context: ContextTypes.DEFAULT_TYPE):
    """Функсия барои фиристодани тести автоматӣ ба ҳамаи корбарон"""
    users = get_all_users()
    
    question = "By next year, we _______ here for ten years."
    options = ["will live", "will be living", "will have been living"]
    correct_option_id = 2  # Варианти 3-юм дуруст аст
    
    for user_id in users:
        try:
            # Фиристодани тест
            await context.bot.send_poll(
                chat_id=user_id,
                question=question,
                options=options,
                type="quiz",
                correct_option_id=correct_option_id,
                explanation="Дарси Future Perfect Continuous-ро ба ёд оред! 😉",
                explanation_parse_mode="Markdown"
            )
            
            # Рекламаи канал
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📚 Тестҳои бештар ва китобҳо дар канали мо:\n👉 {CHANNEL_USERNAME}"
            )
        except Exception as e:
            print(f"Хатогӣ ҳангоми фиристодан ба {user_id}: {e}")

def start_scheduler(application):
    """Ба кор андохтани таймер тавассути JobQueue-и дохилӣ"""
    job_queue = application.job_queue
    
    # Танзими вақт: Ҳар рӯз соати 09:00 (бо вақти Душанбе)
    # Агар сервери Render бо вақти UTC кор кунад, соати 04:00-и UTC баробари 09:00-и Душанбе мешавад.
    target_time = datetime.time(hour=4, minute=0, second=0) 
    
    job_queue.run_daily(send_daily_test, time=target_time)
