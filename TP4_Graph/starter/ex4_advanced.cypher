// 4.1 Trouver un tuteur
// Étudiant qui maîtrise Python et a eu >14/20 en 'Bases de Données Avancées'
MATCH (tuteur:Etudiant)-[:MAITRISE]->(:Competence {nom: "Python"})
MATCH (tuteur)-[s:SUIT]->(c:Cours {intitule: "Bases de Données Avancées"})
WHERE s.note > 14
RETURN tuteur.prenom, tuteur.nom, s.note;

// 4.2 Réseau alumni
// "Qui de mon réseau (jusqu'à 3 sauts) travaille chez Sonatrach ?"
// (Note: On simule une entreprise Sonatrach si non présente)
MERGE (sonatrach:Entreprise {nom: "Sonatrach", secteur: "Energie"});
MATCH (e:Etudiant {prenom: "Prenom1"})-[:CONNAIT*1..3]-(alumni:Etudiant)-[:A_STAGE_CHEZ]->(sonatrach)
RETURN DISTINCT alumni.prenom, alumni.nom;

// 4.3 Détection de ponts (étudiants connectant des universités différentes)
MATCH (e:Etudiant)-[:CONNAIT]-(ami:Etudiant)
WHERE e.universite <> ami.universite
RETURN e.prenom, e.universite, count(ami) AS nb_connexions_externes
ORDER BY nb_connexions_externes DESC
LIMIT 5;

// 4.4 Analyse temporelle (nouvelles connexions par année/contexte)
MATCH ()-[r:CONNAIT]->()
RETURN r.depuis AS annee, count(r) AS nb_connexions
ORDER BY annee;

// 4.5 Score de similarité (Jaccard) entre deux étudiants (Prenom1 et Prenom2)
// Basé sur les cours suivis en commun
MATCH (e1:Etudiant {prenom: "Prenom1"})-[:SUIT]->(c:Cours)
WITH e1, collect(id(c)) AS c1
MATCH (e2:Etudiant {prenom: "Prenom2"})-[:SUIT]->(c:Cours)
WITH e1, c1, e2, collect(id(c)) AS c2
WITH c1, c2, 
     [x IN c1 WHERE x IN c2] AS intersection,
     [x IN c1 + c2 | x] AS union_raw
WITH size(intersection) AS inter_size, size(apoc.coll.toSet(union_raw)) AS union_size
RETURN inter_size, union_size, toFloat(inter_size) / union_size AS similarity_jaccard;
