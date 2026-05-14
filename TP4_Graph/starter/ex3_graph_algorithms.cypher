MATCH p = shortestPath((a:Etudiant {prenom: "Prenom1"})-[:CONNAIT*..10]-(b:Etudiant {prenom: "Prenom5"}))
RETURN [n IN nodes(p) | n.prenom + " (" + n.universite + ")"] AS chemin, length(p) AS nb_intermediaires;

CALL gds.graph.project('reseau_social', 'Etudiant', 'CONNAIT');

CALL gds.degree.stream('reseau_social')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).prenom AS etudiant, score AS nb_connexions
ORDER BY score DESC
LIMIT 10;

CALL gds.louvain.stream('reseau_social')
YIELD nodeId, communityId
WITH communityId, collect(gds.util.asNode(nodeId).prenom) AS membres
RETURN communityId, size(membres) AS taille, membres[0..5] AS exemple_membres
ORDER BY taille DESC;

MATCH (moi:Etudiant {prenom: "Prenom1"})
MATCH (suggestion:Etudiant) WHERE NOT (moi)-[:CONNAIT]-(suggestion) AND moi <> suggestion
OPTIONAL MATCH (moi)-[:CONNAIT]-(ami)-[:CONNAIT]-(suggestion)
WITH moi, suggestion, count(ami) AS amis_communs
OPTIONAL MATCH (moi)-[:SUIT]->(c)<-[:SUIT]-(suggestion)
WITH moi, suggestion, amis_communs, count(c) AS cours_communs
WITH suggestion, (amis_communs * 3 + cours_communs * 2 + iif(moi.filiere = suggestion.filiere, 1, 0)) AS score
RETURN suggestion.prenom AS suggestion, score
ORDER BY score DESC
LIMIT 5;

MATCH path = (debut:Cours)-[:REQUIERT*]->(but:Competence {nom: "Machine Learning"})
RETURN [n IN nodes(path) | CASE WHEN n:Cours THEN n.intitule ELSE n.nom END] AS parcours_apprentissage;

CALL gds.graph.drop('reseau_social');

