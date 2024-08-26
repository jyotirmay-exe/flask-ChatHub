import random
import string
import hashlib
from datetime import datetime

def generate_room_id(length=6):  
    characters = string.ascii_letters + string.digits
    room_id = ''.join(random.choice(characters) for _ in range(length)).upper()
    
    return room_id

def hasher(s, algorithm='sha256'):    
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(s.encode())
        hash_value = hasher.hexdigest()
        return hash_value
    except ValueError as e:
        raise

def getDate(date_format="%d/%m/%y"):    
    try:
        current_date = datetime.now().strftime(date_format)
        return current_date
    except Exception as e:
        raise

def getTime(time_format="%H:%M"):    
    try:
        current_time = datetime.now().strftime(time_format)
        return current_time
    except Exception as e:
        raise
