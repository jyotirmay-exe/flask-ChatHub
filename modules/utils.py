import random
import string
import hashlib
from datetime import datetime

def generate_room_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length)).upper()

def hasher(s, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    hasher.update(s.encode())
    return hasher.hexdigest()

def getDate():
    return datetime.now().strftime("%d/%m/%Y")

def getTime():
    return datetime.now().strftime("%H:%M")