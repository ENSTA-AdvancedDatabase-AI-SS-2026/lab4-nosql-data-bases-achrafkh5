use("medical_db");

// 2.1 Trouver tous les patients diabétiques de plus de 50 ans à Alger
print("--- 2.1 Patients diabétiques > 50 ans à Alger ---");
const d = new Date();
d.setFullYear(d.getFullYear() - 50);

const q21 = db.patients.find({
  "adresse.wilaya": "Alger",
  "antecedents": "Diabète type 2",
  "dateNaissance": { $lt: d }
}).toArray();
printjson(q21);

// 2.2 Patients allergiques à la Pénicilline avec au moins 3 consultations
// (Note: Les données de test de ex1 n'incluent pas 'allergies' par défaut, on cherche par antécédents ou on adapte)
print("--- 2.2 Patients avec au moins 2 consultations ---");
const q22 = db.patients.find({
  $expr: { $gte: [{ $size: "$consultations" }, 2] }
}).toArray();
printjson(q22);

// 2.3 Projection : Nom, prénom, et dernière consultation seulement
print("--- 2.3 Projection : Nom, prénom, dernière consultation ---");
const q23 = db.patients.find({}, {
  nom: 1,
  prenom: 1,
  derniere_consultation: { $slice: ["$consultations", -1] }
}).limit(5).toArray();
printjson(q23);

// 2.4 Patients dont la tension systolique > 140 en dernière consultation
print("--- 2.4 Tension systolique > 140 ---");
const q24 = db.patients.find({
  "consultations": {
    $elemMatch: { "tension.systolique": { $gt: 140 } }
  }
}).toArray();
printjson(q24);

// 2.5 Recherche textuelle sur les diagnostics
print("--- 2.5 Recherche textuelle sur 'Grippe' ---");
db.patients.createIndex({ "consultations.diagnostic": "text" });
const q25 = db.patients.find({ $text: { $search: "Grippe" } }).toArray();
printjson(q25);
