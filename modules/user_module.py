import sqlite3

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

def authenticate_user(username, password):
    db = get_db()
    row = db.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    ).fetchone()
    return User(row['id'], row['username'], row['password'], row['role']) if row else None

def register_user(username, password):
    db = get_db()
    db.execute(
        'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
        (username, password, 'employee')
    )
    db.commit()
