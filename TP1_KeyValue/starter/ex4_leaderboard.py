import redis
from typing import Optional

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

LEADERBOARD_KEY = "leaderboard:sales"

def record_sale(r, product_id, quantity: int = 1):
    r.zincrby(LEADERBOARD_KEY, quantity, product_id)

def get_top_products(r, n: int = 10) -> list:
    data = r.zrevrange(LEADERBOARD_KEY, 0, n - 1, withscores=True)
    return [{"product_id": pid, "sales": score} for pid, score in data]

def get_product_rank(r, product_id) -> Optional[int]:
    rank = r.zrevrank(LEADERBOARD_KEY, product_id)
    return rank + 1 if rank is not None else None

def get_products_between_ranks(r, start_rank: int, end_rank: int) -> list:
    data = r.zrevrange(LEADERBOARD_KEY, start_rank - 1, end_rank - 1, withscores=True)
    return [{"product_id": pid, "sales": score} for pid, score in data]

def simulate_sales_day(r, n_sales: int = 500):
    import random
    products = list(range(1, 21))
    for _ in range(n_sales):
        product_id = random.choice(products)
        qty = random.randint(1, 5)
        record_sale(r, product_id, qty)

if __name__ == "__main__":
    r.flushdb()
    
    simulate_sales_day(r, 500)
    
    print("\n🏆 Top 5 produits:")
    for i, p in enumerate(get_top_products(r, 5), 1):
        print(f"  {i}. Produit #{p['product_id']} — {int(p['sales'])} ventes")
    
    print(f"\nRang du produit #1: {get_product_rank(r, 1)}")

