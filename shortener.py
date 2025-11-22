import string
from secrets import choice

ALPHABET = string.ascii_letters + string.digits

def generate_slug() -> str:
    res = ""
    for _ in range(6):
        res += choice(ALPHABET)
    return res
