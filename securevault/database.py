import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'securevault.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                      (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password_hash = ?',
                  (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def save_password(user_id, website, username, encrypted_password, category='General'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (user_id, website, username, encrypted_password, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, website, username, encrypted_password, category))
    conn.commit()
    conn.close()

def get_passwords(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, website, username, encrypted_password, category, created_at 
        FROM passwords WHERE user_id = ?
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_password(password_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
    conn.commit()
    conn.close()

def update_password(password_id, website, username, encrypted_password, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE passwords 
        SET website = ?, username = ?, encrypted_password = ?, category = ?
        WHERE id = ?
    ''', (website, username, encrypted_password, category, password_id))
    conn.commit()
    conn.close()

def search_passwords(user_id, keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, website, username, encrypted_password, category, created_at 
        FROM passwords 
        WHERE user_id = ? AND (website LIKE ? OR username LIKE ?)
    ''', (user_id, f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_password_by_id(password_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, website, username, encrypted_password, category 
        FROM passwords WHERE id = ?
    ''', (password_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_passwords_by_category(user_id, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, website, username, encrypted_password, category, created_at 
        FROM passwords 
        WHERE user_id = ? AND category = ?
    ''', (user_id, category))
    rows = cursor.fetchall()
    conn.close()
    return rows
def get_all_categories(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT category FROM passwords WHERE user_id = ?
    ''', (user_id,))
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories