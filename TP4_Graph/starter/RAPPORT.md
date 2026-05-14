# Rapport TP4 — Neo4j Réseau Social Universitaire

## 1. Schéma du Graphe (Data Model)

Le graphe est composé de :
*   **Nœuds :** Etudiant, Cours, Competence, Entreprise, Club.
*   **Relations :** 
    *   `CONNAIT` (Etudiant -> Etudiant) : Relation réflexive pour le réseau social.
    *   `SUIT` (Etudiant -> Cours) : Inscription aux modules.
    *   `MAITRISE` (Etudiant -> Competence) : Compétences acquises.

## 2. Analyse des Communautés (Louvain)

L'algorithme de Louvain a identifié plusieurs communautés basées sur la relation `CONNAIT`. 
*   **Observation :** Les étudiants d'une même université ou filière ont tendance à former des clusters denses.
*   **Utilité :** Cela permet à UniConnect de suggérer des groupes d'étude ou des événements ciblés par communauté.

## 3. Comparaison SQL vs Cypher

Pour trouver les "Amis d'Amis" (2 sauts) :

*   **SQL :**
    ```sql
    SELECT DISTINCT e3.* FROM Etudiants e1
    JOIN Relations r1 ON e1.id = r1.from_id
    JOIN Relations r2 ON r1.to_id = r2.from_id
    JOIN Etudiants e3 ON r2.to_id = e3.id
    WHERE e1.prenom = 'Ahmed' AND e3.id <> e1.id;
    ```
*   **Cypher :**
    ```cypher
    MATCH (:Etudiant {prenom: 'Ahmed'})-[:CONNAIT*2]-(fof:Etudiant)
    RETURN fof;
    ```

**Conclusion :** Cypher est beaucoup plus lisible et performant pour les parcours de graphe. En SQL, chaque niveau de profondeur supplémentaire nécessite un `JOIN` supplémentaire, ce qui dégrade rapidement les performances et la lisibilité du code.
