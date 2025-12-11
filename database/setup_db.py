import sqlite3

LOGIN_DB = 'login.db'

def setup_login_db():
    conn = sqlite3.connect(LOGIN_DB)
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Insert initial login users (Admin, Doctor, Viewer)
    users = [
        ('admin', '1234', 'administrator'),
        ('doctor', 'pass', 'doctor'),
        ('user', 'view', 'viewer'),
    ]
    
    # Check if users already exist before inserting
    for user_id, password, role in users:
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, password, role))
            print(f"User {user_id} created.")
        else:
            print(f"User {user_id} already exists.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_login_db()
    print("Login database setup complete.")