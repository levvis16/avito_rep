import random
import uuid

def generate_seller_id():
    return random.randint(111111, 999999)

def generate_item_name():
    return f"Item_{uuid.uuid4().hex[:8]}"

def generate_price(min_price=1, max_price=999999):
    return random.randint(min_price, max_price)

def generate_statistics(likes=0, view_count=0, contacts=0):
    return {"likes": likes, "viewCount": view_count, "contacts": contacts}

def generate_invalid_id():
    return str(uuid.uuid4())