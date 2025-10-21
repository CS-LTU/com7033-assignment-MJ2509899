import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_auth_db():
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, hashed_pw))
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect('auth.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    row = c.fetchone()
    conn.close()
    if row and bcrypt.check_password_hash(row[0], password):
        return True
    return False
