import sqlite3
import time

def create_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.commit()
    conn.close()

def add_user(name, age):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    c.execute(query, (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def retry_with_backoff(func, *args, **kwargs):
    max_retries = 5
    delay = 1  # Initial delay in seconds
    for retry in range(max_retries):
        try:
            return func(*args, **kwargs)
        except sqlite3.OperationalError as e:
            if "too many connections" in str(e):
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e
    raise Exception("Max retries exceeded")