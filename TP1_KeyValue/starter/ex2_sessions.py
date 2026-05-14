import redis
import uuid
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

SESSION_TTL = 1800  # 30 minutes en secondes

def create_session(r, user_id: str) -> str:
    """Crée une session pour un utilisateur avec un TTL de 30 min."""
    session_id = str(uuid.uuid4())
    session_key = f"session:{session_id}"
    
    # Stocker les infos de base
    r.hset(session_key, mapping={
        "user_id": user_id,
        "created_at": time.time(),
        "last_activity": time.time()
    })
    
    # Définir l'expiration
    r.expire(session_key, SESSION_TTL)
    return session_id

def get_session(r, session_id: str) -> dict:
    """Récupère la session et renouvelle le TTL (Sliding Expiration)."""
    session_key = f"session:{session_id}"
    session = r.hgetall(session_key)
    
    if session:
        # Renouveler le TTL (Sliding Expiration)
        r.hset(session_key, "last_activity", time.time())
        r.expire(session_key, SESSION_TTL)
        return session
    return None

def delete_session(r, session_id: str):
    """Supprime une session (logout)."""
    r.delete(f"session:{session_id}")

if __name__ == "__main__":
    r.flushdb()
    
    # Test Création
    sid = create_session(r, "user:123")
    print(f"Session créée: {sid}")
    
    # Test Récupération et Renouvellement
    sess = get_session(r, sid)
    print(f"Session récupérée: {sess}")
    print(f"TTL restant: {r.ttl(f'session:{sid}')} secondes")
    
    # Test Suppression
    delete_session(r, sid)
    print(f"Session supprimée, existe? {r.exists(f'session:{sid}')}")
