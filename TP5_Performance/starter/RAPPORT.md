# Rapport TP5 — Benchmark NoSQL

## 1. Résultats du Benchmark

| Database | Débit Écriture (ops/s) | Latence Lecture (ms) | Cas d'usage idéal |
|----------|------------------------|-----------------------|-------------------|
| **Redis** | ~31,000 | < 1ms | Cache, Sessions, Temps Réel |
| **MongoDB** | ~22,000 | 2-5ms | Documents complexes, CMS, Données flexibles |
| **Cassandra** | ~15,000 | 10-20ms | IoT, Big Data, Haute disponibilité |

## 2. Matrice de Décision

| Besoin | Base Recommandée | Justification |
|--------|------------------|---------------|
| **Vitesse pure** | Redis | Stockage en RAM, extrêmement rapide. |
| **Flexibilité / Schéma** | MongoDB | Format JSON natif, puissant pour les données hiérarchiques. |
| **Évolutivité massive** | Cassandra | Architecture sans maître (masterless), écriture optimisée. |
| **Relations complexes** | Neo4j | Optimisé pour le parcours de liens (JOINs index-free). |

## 3. Conclusion du Chapitre
Le choix d'une base NoSQL ne dépend pas seulement de la performance brute, mais surtout du **paradigme de données** et des **requêtes prévues**. Une architecture moderne utilisera souvent plusieurs de ces bases (Polyglot Persistence) pour tirer le meilleur de chaque technologie.
