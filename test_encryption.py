from securevault.encryption import generate_key, encrypt_password, decrypt_password, hash_password, verify_password

def test_encryption():
    generate_key()

    # Test encrypt and decrypt
    original = "supersecretpassword"
    encrypted = encrypt_password(original)
    decrypted = decrypt_password(encrypted)
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {original == decrypted}")

    # Test hashing
    hashed = hash_password("mypassword")
    print(f"Hash: {hashed}")
    print(f"Verify correct: {verify_password('mypassword', hashed)}")
    print(f"Verify wrong: {verify_password('wrongpassword', hashed)}")

if __name__ == "__main__":
    test_encryption()