// 2.1 Trouver tous les amis de Prenom1
MATCH (:Etudiant {prenom: "Prenom1"})-[:CONNAIT]-(ami:Etudiant)
RETURN ami.prenom, ami.nom, ami.universite;

// 2.2 Trouver les amis d'amis de Prenom1 qui ne sont pas déjà ses amis
MATCH (moi:Etudiant {prenom: "Prenom1"})-[:CONNAIT]-()-[:CONNAIT]-(fof:Etudiant)
WHERE NOT (moi)-[:CONNAIT]-(fof) AND moi <> fof
RETURN DISTINCT fof.prenom, fof.nom;

// 2.3 Étudiants qui suivent le même cours que Prenom10 mais ne la connaissent pas
MATCH (f:Etudiant {prenom: "Prenom10"})-[:SUIT]->(c:Cours)<-[:SUIT]-(autre:Etudiant)
WHERE NOT (f)-[:CONNAIT]-(autre) AND f <> autre
RETURN DISTINCT autre.prenom, c.intitule;

// 2.4 Clubs les plus populaires (par nombre de membres)
MATCH (c:Club)<-[:MEMBRE_DE]-(e:Etudiant)
RETURN c.nom, count(e) AS nb_membres
ORDER BY nb_membres DESC;

// 2.5 Profil complet d'un étudiant (Prenom1)
MATCH (e:Etudiant {prenom: "Prenom1"})
OPTIONAL MATCH (e)-[:CONNAIT]-(ami)
OPTIONAL MATCH (e)-[:SUIT]->(cours)
OPTIONAL MATCH (e)-[:MAITRISE]->(comp)
RETURN e.prenom, e.nom, 
       collect(DISTINCT ami.prenom) AS amis, 
       collect(DISTINCT cours.intitule) AS cours, 
       collect(DISTINCT comp.nom) AS competences;
