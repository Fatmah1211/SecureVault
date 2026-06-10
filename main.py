from securevault.database import initialize_database, register_user, login_user, save_password, get_passwords, delete_password, update_password, search_passwords, get_password_by_id, get_passwords_by_category
from securevault.encryption import generate_key, encrypt_password, decrypt_password, hash_password
from securevault.hibp import check_password_breached

def test():
    # Setup
    generate_key()
    initialize_database()

    # Test registration
    hashed = hash_password("testpass123")
    result = register_user("fatimah", hashed)
    print(f"Registration: {'Success' if result else 'User already exists'}")

    # Test login
    user_id = login_user("fatimah", hashed)
    print(f"Login: {'Success, user_id=' + str(user_id) if user_id else 'Failed'}")

    # Test saving a password
    encrypted = encrypt_password("myFacebookPass123")
    save_password(user_id, "facebook.com", "fatimah@email.com", encrypted, "Social")
    print("Password saved successfully")

    # Test retrieving passwords
    passwords = get_passwords(user_id)
    for p in passwords:
        decrypted = decrypt_password(p[3])
        print(f"Website: {p[1]} | Username: {p[2]} | Password: {decrypted} | Category: {p[4]}")

    # Test HIBP
    count = check_password_breached("password123")
    if count is None:
        print("HIBP API error")
    elif count == 0:
        print("Password is clean")
    else:
        print(f"Password breached {count} times!")
    # Test search
    results = search_passwords(user_id, "face")
    print(f"Search results: {len(results)} found")

    # Test get by id
    entry = get_password_by_id(1)
    print(f"Entry by id: {entry}")

    # Test update
    update_password(1, "facebook.com", "newuser@email.com", encrypt_password("newpass456"), "Social")
    print("Password updated successfully")

    # Test category filter
    social = get_passwords_by_category(user_id, "Social")
    print(f"Social passwords: {len(social)} found")

if __name__ == "__main__":
    test()