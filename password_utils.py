import secrets
import string
import hashlib
import requests

def generate_password(length, use_digits, use_symbols, use_upper):
    # Always include lowercase
    characters = string.ascii_lowercase

    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    # Safety check — if somehow nothing is selected
    if not characters:
        characters = string.ascii_lowercase

    # Using secrets.choice instead of random.choices for cryptographic security
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    variety = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 16 and variety == 4:
        return "Strong"
    elif length >= 12 and variety >= 3:
        return "Medium"
    else:
        return "Weak"

def check_hibp(password):
    # Hash the password using SHA1
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    # Send only the first 5 characters to the API
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code != 200:
            return "error"

        # Check if our suffix appears in the results
        hashes = response.text.splitlines()
        for line in hashes:
            h, count = line.split(":")
            if h == suffix:
                return int(count)

        return 0

    except requests.exceptions.ConnectionError:
        return "offline"