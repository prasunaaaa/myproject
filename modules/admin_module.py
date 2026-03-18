import sqlite3

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TASK
def create_task(title, assigned_to, due_date):
    db = get_db()
    db.execute(
        'INSERT INTO tasks (title, status, assigned_to, due_date) VALUES (?, ?, ?, ?)',
        (title, 'Pending', assigned_to, due_date)
    )
    db.commit()

# UPDATE / EDIT TASK
def update_task(task_id, title, assigned_to, due_date, status):
    db = get_db()
    db.execute(
        '''UPDATE tasks 
           SET title=?, assigned_to=?, due_date=?, status=? 
           WHERE id=?''',
        (title, assigned_to, due_date, status, task_id)
    )
    db.commit()

# DELETE TASK
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    db.commit()

# GET USERS (for assignment)
def get_all_users():
    db = get_db()
    return db.execute('SELECT username FROM users').fetchall()
