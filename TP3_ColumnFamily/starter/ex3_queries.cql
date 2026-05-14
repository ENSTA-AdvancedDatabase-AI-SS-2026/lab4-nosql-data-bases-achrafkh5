USE smartgrid;

-- 3.1 Mesures d'un capteur spécifique sur les dernières 6 heures
-- Remarque : Nécessite de connaître le capteur_id et la date
SELECT * FROM mesures_par_capteur 
WHERE capteur_id = 550e8400-e29b-41d4-a716-446655440000 
  AND date_jour = '2024-05-14' 
  AND timestamp >= '2024-05-14 18:00:00';

-- 3.2 Dernière mesure d'un capteur (utilisant le clustering order DESC)
SELECT * FROM mesures_par_capteur 
WHERE capteur_id = 550e8400-e29b-41d4-a716-446655440000 
  AND date_jour = '2024-05-14' 
LIMIT 1;

-- 3.3 Capteurs en alerte dans la wilaya "Alger" aujourd'hui
SELECT * FROM alertes_par_wilaya 
WHERE wilaya = 'Alger' 
  AND date_jour = '2024-05-14';

-- 3.4 Agrégats horaires pour une wilaya
SELECT * FROM agregats_horaires 
WHERE wilaya = 'Alger' 
  AND date_heure >= '2024-05-14 00:00:00' 
  AND date_heure <= '2024-05-14 23:59:59';

-- 3.5 Détection d'anomalie (Tension < 200V ou > 240V)
-- Cassandra ne supporte pas l'opérateur OR. On effectue deux requêtes séparées.
SELECT * FROM mesures_par_capteur WHERE tension_v < 200 ALLOW FILTERING;
SELECT * FROM mesures_par_capteur WHERE tension_v > 240 ALLOW FILTERING;

-- 3.6 Nombre total d'alertes par wilaya
-- Nécessite ALLOW FILTERING car on groupe sur une colonne qui n'est pas la clé de partition entière sans filtre
SELECT wilaya, count(*) FROM alertes_par_wilaya 
WHERE date_jour = '2024-05-14' 
GROUP BY wilaya 
ALLOW FILTERING;

-- 3.7 Pourquoi éviter ALLOW FILTERING ?
-- R: ALLOW FILTERING force Cassandra à scanner toutes les partitions sur tous les nœuds, 
-- ce qui annule les bénéfices de distribution et de performance du hachage de la partition key.
-- Pour une alternative performante : utiliser une table indexée par la valeur (ex: alertes_par_gravite).
