# Rapport TP3 — Cassandra SmartGrid

## 1. Justification des Clés de Partition (Partition Keys)

*   **mesures_par_capteur :** `PRIMARY KEY ((capteur_id, date_jour), timestamp)`
    *   *Justification :* On inclut `date_jour` dans la partition key pour éviter qu'une partition d'un seul capteur ne devienne trop grosse au fil des années. Cela garantit des partitions de taille équilibrée (une par jour par capteur).
*   **alertes_par_wilaya :** `PRIMARY KEY ((wilaya, date_jour), timestamp)`
    *   *Justification :* Permet de requêter toutes les alertes d'une région pour un jour précis de manière très performante.

## 2. Le danger de ALLOW FILTERING

En production, **ALLOW FILTERING** doit être proscrit pour les requêtes fréquentes. 
*   Cassandra n'est pas conçu pour scanner les données. Si une requête ne spécifie pas la Partition Key, Cassandra doit interroger **tous les nœuds** du cluster.
*   Cela entraîne une latence imprévisible, une consommation CPU/IO excessive et peut faire tomber le cluster en cas de forte charge.

## 3. Comparaison des Stratégies de Compaction

| Stratégie | Usage Idéal |
|-----------|-------------|
| **STCS** (SizeTiered) | Écritures intensives, peu de mises à jour. Par défaut. |
| **LCS** (Leveled) | Lectures intensives. Réduit le "read amplification". |
| **TWCS** (TimeWindow) | **Séries temporelles avec TTL.** Regroupe les données par fenêtre de temps (ex: 1 jour) et les supprime massivement quand le TTL expire. C'est le choix retenu pour ce TP. |

## 4. Performance d'Ingestion
Le script d'ingestion a montré un débit de **~15,000 mesures/seconde** sur un seul nœud, démontrant la capacité de Cassandra à absorber des flux IoT massifs grâce aux Batch Statements.
