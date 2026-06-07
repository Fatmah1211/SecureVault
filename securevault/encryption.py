import hashlib
import os
from cryptography.fernet import Fernet

KEY_PATH = os.path.join(os.path.dirname(__file__), '..', 'secret.key')

def generate_key():
    if not os.path.exists(KEY_PATH):
        key = Fernet.generate_key()
        with open(KEY_PATH, 'wb') as f:
            f.write(key)

def load_key():
    with open(KEY_PATH, 'rb') as f:
        return f.read()

def encrypt_password(plain_password):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(plain_password.encode()).decode()

def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed