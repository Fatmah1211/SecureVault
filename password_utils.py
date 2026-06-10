import random
import string

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

    password = ''.join(random.choices(characters, k=length))
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