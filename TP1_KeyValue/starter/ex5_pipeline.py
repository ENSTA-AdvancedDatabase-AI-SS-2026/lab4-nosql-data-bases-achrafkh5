import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def bulk_insert_products(r, products: list):
    """Insère plusieurs produits efficacement avec un Pipeline."""
    pipe = r.pipeline()
    for p_id, p_data in products:
        pipe.hset(f"product:{p_id}", mapping=p_data)
    pipe.execute()

def process_order_transaction(r, user_id: str, product_id: str, quantity: int):
    """Gère une commande de manière atomique avec une Transaction (MULTI/EXEC)."""
    product_key = f"product:{product_id}"
    cart_key = f"cart:{user_id}"
    
    with r.pipeline() as pipe:
        while True:
            try:
                # Surveiller le stock pour éviter les conditions de concurrence
                pipe.watch(product_key)
                
                stock = int(pipe.hget(product_key, "stock") or 0)
                if stock < quantity:
                    pipe.unwatch()
                    return False, "Stock insuffisant"
                
                # Début de la transaction
                pipe.multi()
                pipe.hincrby(product_key, "stock", -quantity)
                pipe.hincrby(cart_key, product_id, quantity)
                
                # Exécution
                pipe.execute()
                return True, "Commande réussie"
                
            except redis.WatchError:
                # Réessayer si le stock a changé entre temps
                continue

if __name__ == "__main__":
    r.flushdb()
    
    # 1. Test Bulk Insert
    products = [
        (101, {"name": "Souris Gamer", "price": 4500, "stock": 20}),
        (102, {"name": "Tapis Souris", "price": 1200, "stock": 50}),
        (103, {"name": "Ecran 24p", "price": 28000, "stock": 5})
    ]
    bulk_insert_products(r, products)
    print("Produits insérés par pipeline.")
    
    # 2. Test Transaction (Succès)
    success, msg = process_order_transaction(r, "user:456", "103", 2)
    print(f"Transaction (2 écrans): {msg}, Nouveau stock: {r.hget('product:103', 'stock')}")
    
    # 3. Test Transaction (Échec stock)
    success, msg = process_order_transaction(r, "user:456", "103", 10)
    print(f"Transaction (10 écrans): {msg}")
