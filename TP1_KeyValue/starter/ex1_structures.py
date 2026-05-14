import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def store_product(r, product_id, product_data: dict):
    r.hset(f"product:{product_id}", mapping=product_data)

def get_product(r, product_id):
    data = r.hgetall(f"product:{product_id}")
    return data if data else None

def add_to_cart(r, user_id, product_id, quantity: int = 1):
    r.hincrby(f"cart:{user_id}", product_id, quantity)

def get_cart(r, user_id):
    return r.hgetall(f"cart:{user_id}")

def record_view(r, user_id, product_id, max_history: int = 10):
    r.lpush(f"history:{user_id}", product_id)
    r.ltrim(f"history:{user_id}", 0, max_history - 1)

def get_history(r, user_id):
    return r.lrange(f"history:{user_id}", 0, -1)

def add_product_to_category(r, category: str, product_id):
    r.sadd(f"category:{category}", product_id)

def get_products_in_categories(r, *categories):
    keys = [f"category:{c}" for c in categories]
    return r.sinter(keys)

if __name__ == "__main__":
    r.flushdb()
    
    store_product(r, 1, {"name": "Samsung A54", "price": "65000", "category": "phones", "stock": "15"})
    store_product(r, 2, {"name": "Laptop HP", "price": "120000", "category": "laptops", "stock": "8"})
    
    add_to_cart(r, "user:42", 1, 2)
    add_to_cart(r, "user:42", 2, 1)
    print("Panier:", get_cart(r, "user:42"))
    
    for pid in [1, 2, 1, 3, 2]:
        record_view(r, "user:42", pid)
    print("Historique:", get_history(r, "user:42"))

