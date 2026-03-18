from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from modules import user_module
from modules import task_module
from modules import admin_module

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Database Initialization
def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             username TEXT UNIQUE, 
             password TEXT, 
             role TEXT)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title TEXT, 
             status TEXT, 
             assigned_to TEXT, 
             due_date TEXT)''')
        
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
        except:
            pass
        conn.commit()

# 1. NEW WELCOME PAGE (Root Route)
@app.route('/')
def index():
    return render_template('welcome.html')

# 2. LOGIN PAGE ROUTE
@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    if user:
        session['user'] = user['username']
        session['role'] = user['role']
        return redirect(url_for('dashboard'))
    return "Invalid credentials! <a href='/login_page'>Try again</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']
        db = get_db()
        db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (un, pw, 'employee'))
        db.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login_page'))
    db = get_db()
    if session['role'] == 'admin':
        tasks = db.execute('SELECT * FROM tasks').fetchall()
        users = db.execute('SELECT username FROM users').fetchall()
        return render_template('admin.html', tasks=tasks, users=users)
    else:
        tasks = db.execute('SELECT * FROM tasks WHERE assigned_to = ?', (session['user'],)).fetchall()
        return render_template('dashboard.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if session.get('role') == 'admin':
        title = request.form['title']
        assigned_to = request.form['assigned_to']
        due_date = request.form.get('due_date')

        # Date Validation
        is_valid, message = task_module.is_valid_date(due_date)
        if not is_valid:
            return f"<script>alert('{message}'); window.history.back();</script>"

        db = get_db()
        db.execute('INSERT INTO tasks (title, status, assigned_to, due_date) VALUES (?, ?, ?, ?)', 
                   (title, 'Pending', assigned_to, due_date))
        db.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_task/<int:id>')
def update_task(id):
    db = get_db()
    db.execute('UPDATE tasks SET status = "Completed" WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)