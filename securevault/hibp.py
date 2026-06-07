import hashlib
import requests

def check_password_breached(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    hashes = response.text.splitlines()
    for line in hashes:
        h, count = line.split(':')
        if h == suffix:
            return int(count)

    return 0
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
    cursor.execute('SELECT id, website, username, encrypted_password, category, created_at FROM passwords WHERE user_id = ?', 
                  (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_password(password_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
    conn.commit()
    conn.close()