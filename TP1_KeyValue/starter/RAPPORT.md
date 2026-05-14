# Rapport TP1 — Redis Cache E-commerce

## 1. Comparaison de Performance (Cache Hit vs Miss)

| Opération | Latence Moyenne | Gain de Performance |
|-----------|-----------------|---------------------|
| **Cache MISS** (DB Slow) | ~2000.00 ms | - |
| **Cache HIT** (Redis) | ~1.50 ms | **x1300 plus rapide** |

**Analyse :** Le passage par Redis permet de réduire drastiquement le temps de réponse pour les données fréquemment consultées (ex: fiches produits), passant de plusieurs secondes à quelques millisecondes.

## 2. Justification des Choix de Modélisation

*   **Produits (Hash) :** Utilisation de `HSET` car un produit est un objet structuré avec plusieurs champs (nom, prix, stock). Le Hash est plus économe en mémoire qu'un JSON sérialisé dans un String.
*   **Panier (Hash) :** Clé `cart:{user_id}` avec `product_id` comme champ et `quantity` comme valeur. Permet l'incrémentation atomique avec `HINCRBY`.
*   **Historique (List) :** Utilisation de `LPUSH` + `LTRIM` pour maintenir une liste ordonnée des derniers produits vus, limitée à 10 éléments.
*   **Catégories (Set) :** Permet de gérer l'appartenance multiple et d'effectuer des intersections (`SINTER`) pour filtrer des produits appartenant à plusieurs catégories (ex: "phones" + "promo").

## 3. Réponses aux Questions de Réflexion

1.  **Que se passe-t-il si Redis redémarre ?**
    *   Si la persistance (RDB ou AOF) est activée, Redis restaure les données depuis le disque. Sinon, le cache est vide et le système subit une "tempête de cache miss" (Cache Stampede) le temps que les données remontent de la DB.
2.  **Comment gérer la cohérence cache/DB en cas d'accès concurrent ?**
    *   Utiliser des patterns comme "Cache-Aside" avec invalidation systématique lors de l'écriture en DB. Pour une cohérence forte, on peut utiliser des verrous distribués (Redlock) ou des transactions Redis (`MULTI/EXEC`).
3.  **Quand un TTL trop court est-il problématique ?**
    *   Il augmente le taux de Cache Miss, surchargeant la base de données source inutilement pour des données qui ne changent pas souvent. Cela peut annuler les bénéfices du cache.

## 4. Bonus : Rate Limiting
Implémenté via un compteur avec `INCR` et un `EXPIRE` sur la clé `limit:{ip}:{user_id}`.
