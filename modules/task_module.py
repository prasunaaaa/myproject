import sqlite3
from datetime import datetime  

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_valid_date(task_date_str):
    try:
        input_date = datetime.strptime(task_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        
        if input_date < today:
            return False, "Past date select garna mildaina!"
        return True, "Valid"
    except (ValueError, TypeError):
        return False, "Invalid date format!"

def get_all_tasks():
    db = get_db()
    return db.execute('SELECT * FROM tasks').fetchall()

def get_tasks_by_user(username):
    db = get_db()
    return db.execute(
        'SELECT * FROM tasks WHERE assigned_to=?',
        (username,)
    ).fetchall()