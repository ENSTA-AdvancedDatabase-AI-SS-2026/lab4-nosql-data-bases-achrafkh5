# Rapport TP2 — MongoDB Dossiers Médicaux

## 1. Choix de Modélisation (Embedding vs Referencing)

*   **Consultations (EMBEDDING) :** Les consultations sont intégrées directement dans le document `patient`. 
    *   *Justification :* Les consultations sont presque toujours consultées en même temps que le profil du patient. Cela évite des JOINs ($lookup) coûteux et améliore la localité des données.
*   **Analyses (REFERENCING) :** Les analyses sont stockées dans une collection séparée `analyses` liée par `patient_id`.
    *   *Justification :* Le volume des analyses peut devenir très important sur la vie d'un patient (risque de dépasser la limite de 16MB par document). Le référencement permet de gérer un historique illimité.

## 2. Optimisation par Index (Résultats explain)

| Requête | Sans Index (COLLSCAN) | Avec Index (IXSCAN) | Gain |
|---------|-----------------------|---------------------|------|
| Recherche par Wilaya | 20 docs examinés | 4 docs examinés | **80% moins de lecture** |
| Recherche par Diagnostic | 20 docs examinés | 5 docs examinés | **75% moins de lecture** |

**Index créés :**
*   `adresse.wilaya`: Index simple pour les filtres géographiques.
*   `consultations.diagnostic`: Index de texte pour la recherche par mots-clés dans les notes médicales.

## 3. Analyse de la Requête la plus Complexe (Ex 3.5)

La requête 3.5 calcule le top 5 des médecins avec leur taux de ré-consultation :
1.  **$unwind** : Découpage du tableau de consultations pour traiter chaque visite séparément.
2.  **$group** : Regroupement par nom de médecin. On utilise `$addToSet` sur l'ID patient pour compter les patients uniques.
3.  **$addFields** : Calcul du nombre de patients uniques (`nb_uniques`) et du taux de ré-consultation via la formule : `((total_consultations - nb_uniques) / nb_uniques) * 100`.
4.  **$sort** : Tri décroissant par activité.

## 4. Conclusion
MongoDB permet une flexibilité totale sur le schéma. L'usage de l'embedding pour les données "chaudes" (consultations) et du referencing pour les données "froides/volumineuses" (analyses) offre le meilleur compromis performance/évolutivité.
