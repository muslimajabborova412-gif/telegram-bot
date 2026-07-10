import sqlite3

DB_NAME = "bot_users.db"

def init_db():
    """Сохтани ҷадвал барои нигоҳ доштани корбарон"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    """Илова кардани корбари нав"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        conn.commit()
    except Exception as e:
        print(f"Хатогӣ дар иловаи корбар: {e}")
    finally:
        conn.close()

def get_all_users():
    """Гирифтани рӯйхати ҳамаи корбарон барои реклама ва автопостинг"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users
