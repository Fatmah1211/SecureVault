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
