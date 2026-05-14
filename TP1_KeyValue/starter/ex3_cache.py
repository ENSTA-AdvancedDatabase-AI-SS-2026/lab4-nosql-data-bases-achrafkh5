import redis
import json
import time
from typing import Optional

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def slow_db_get_product(product_id: int) -> Optional[dict]:
    time.sleep(2)
    products = {
        1: {"id": 1, "name": "Samsung Galaxy A54", "price": 65000, "stock": 15},
        2: {"id": 2, "name": "Laptop HP 15-inch", "price": 120000, "stock": 8},
        3: {"id": 3, "name": "Casque JBL Bluetooth", "price": 12000, "stock": 50},
        4: {"id": 4, "name": "Clavier Mécanique", "price": 8000, "stock": 30},
    }
    return products.get(product_id)

def get_product_cached(r, product_id: int, ttl: int = 600) -> Optional[dict]:
    start = time.time()
    key = f"product_cache:{product_id}"
    cached_data = r.get(key)
    
    if cached_data:
        elapsed = (time.time() - start) * 1000
        print(f"CACHE HIT ({elapsed:.2f}ms)")
        return json.loads(cached_data)
    
    product = slow_db_get_product(product_id)
    if product:
        r.setex(key, ttl, json.dumps(product))
    
    elapsed = (time.time() - start) * 1000
    print(f"CACHE MISS ({elapsed:.2f}ms)")
    return product

def invalidate_product_cache(r, product_id: int):
    r.delete(f"product_cache:{product_id}")

def benchmark_cache(r, product_id: int, iterations: int = 20):
    hits = 0
    hit_times = []
    miss_times = []
    
    for i in range(iterations):
        start = time.time()
        key = f"product_cache:{product_id}"
        cached_data = r.get(key)
        
        if cached_data:
            hits += 1
            hit_times.append((time.time() - start) * 1000)
        else:
            product = slow_db_get_product(product_id)
            if product:
                r.setex(key, 600, json.dumps(product))
            miss_times.append((time.time() - start) * 1000)
            
    print(f"Temps moyen HIT: {sum(hit_times)/len(hit_times) if hit_times else 0:.2f}ms")
    print(f"Temps moyen MISS: {sum(miss_times)/len(miss_times) if miss_times else 0:.2f}ms")
    print(f"Taux HIT: {(hits/iterations)*100:.1f}%")

if __name__ == "__main__":
    r.flushdb()
    
    print("=== Test Cache-Aside ===")
    get_product_cached(r, 1)
    get_product_cached(r, 1)
    
    print("\n=== Benchmark ===")
    benchmark_cache(r, 1, iterations=5)

