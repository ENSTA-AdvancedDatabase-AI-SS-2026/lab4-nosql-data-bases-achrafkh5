USE smartgrid;

-- 4.1 Stratégie de compaction
-- Choix : TimeWindowCompactionStrategy (TWCS)
-- Justification : Idéal pour les séries temporelles où les données sont écrites avec un timestamp
-- et souvent supprimées/expirées (TTL) par groupes temporels. TWCS regroupe les SSTables par
-- fenêtres de temps, ce qui rend le "compaction" et le "cleanup" beaucoup plus efficaces.

-- 4.2 Configurer TWCS pour les mesures (fenêtre de 1 jour)
ALTER TABLE mesures_par_capteur
WITH compaction = {
  'class': 'TimeWindowCompactionStrategy',
  'compaction_window_unit': 'DAYS',
  'compaction_window_size': 1
};

-- 4.3 Vérifier l'utilisation des TTL
-- On ne peut pas "compter" ce qui va expirer sans scanner, mais on peut vérifier le TTL d'une ligne
SELECT capteur_id, ttl(tension_v) 
FROM mesures_par_capteur 
LIMIT 10;

-- 4.4 Analyser une partition "hot"
-- Une partition devient "hot" si trop de données sont écrites sur la même clé (ex: wilaya seule).
-- Solution : Utiliser une clé composée (wilaya + date_jour) pour répartir la charge.
-- Pour détecter : utiliser `nodetool tablestats` ou `nodetool toppartitions`.
