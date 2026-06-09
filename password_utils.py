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