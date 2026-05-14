MATCH (n) DETACH DELETE n;

CREATE CONSTRAINT etudiant_id IF NOT EXISTS FOR (e:Etudiant) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT cours_code IF NOT EXISTS FOR (c:Cours) REQUIRE c.code IS UNIQUE;
CREATE CONSTRAINT competence_nom IF NOT EXISTS FOR (c:Competence) REQUIRE c.nom IS UNIQUE;

UNWIND [
  {nom: "Python", categorie: "Programmation"},
  {nom: "Java", categorie: "Programmation"},
  {nom: "SQL", categorie: "Bases de Données"},
  {nom: "NoSQL", categorie: "Bases de Données"},
  {nom: "Machine Learning", categorie: "IA"},
  {nom: "Deep Learning", categorie: "IA"},
  {nom: "React", categorie: "Web"},
  {nom: "Docker", categorie: "DevOps"},
  {nom: "Linux", categorie: "Systèmes"},
  {nom: "Réseaux", categorie: "Infrastructure"}
] AS comp
MERGE (:Competence {nom: comp.nom, categorie: comp.categorie});

UNWIND [
  {code: "INFO401", intitule: "Bases de Données Avancées", credits: 6, dept: "Informatique"},
  {code: "INFO402", intitule: "Intelligence Artificielle", credits: 6, dept: "Informatique"},
  {code: "INFO403", intitule: "Développement Web", credits: 4, dept: "Informatique"},
  {code: "INFO404", intitule: "Systèmes Distribués", credits: 5, dept: "Informatique"},
  {code: "INFO405", intitule: "Cloud Computing", credits: 4, dept: "Informatique"}
] AS cours
MERGE (:Cours {code: cours.code, intitule: cours.intitule, credits: cours.credits, departement: cours.dept});

UNWIND range(1, 50) AS i
WITH i, ["USTHB", "UMBB", "USTO", "UMC", "UBMA"][i % 5] AS uni, ["Informatique", "Mathématiques", "Electronique", "Telecoms", "GL"][i % 5] AS filiere
MERGE (e:Etudiant {id: "E" + i})
SET e.prenom = "Prenom" + i, e.nom = "Nom" + i, e.universite = uni, e.filiere = filiere, e.annee = 3, e.ville = "Alger";

MATCH (e1:Etudiant), (e2:Etudiant)
WHERE e1.id <> e2.id AND abs(
    (CASE WHEN substring(e1.id, 1) = "" THEN 0 ELSE toInteger(substring(e1.id, 1)) END) - 
    (CASE WHEN substring(e2.id, 1) = "" THEN 0 ELSE toInteger(substring(e2.id, 1)) END)
) < 3
MERGE (e1)-[:CONNAIT {depuis: 2023}]->(e2);

MATCH (e:Etudiant), (c:Cours)
WITH e, c, rand() AS r
WHERE r < 0.5
MERGE (e)-[:SUIT {note: 10 + rand() * 10}]->(c);

MATCH (e:Etudiant), (comp:Competence)
WITH e, comp, rand() AS r
WHERE r < 0.3
MERGE (e)-[:MAITRISE {niveau: "Intermédiaire"}]->(comp);

MATCH (n) RETURN labels(n)[0] AS type, count(n) AS total ORDER BY total DESC;
MATCH ()-[r]->() RETURN type(r) AS relation, count(r) AS total ORDER BY total DESC;

