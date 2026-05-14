use("medical_db");

// 5.1 Joindre patients et analyses pour récupérer le dossier complet
print("--- 5.1 Dossier complet (Patient + Analyses) ---");
const dossierComplet = db.patients.aggregate([
  {
    $lookup: {
      from: "analyses",
      localField: "_id",
      foreignField: "patient_id",
      as: "dossier_analyses"
    }
  },
  { $limit: 1 }
]).toArray();
printjson(dossierComplet);

// 5.2 Trouver les patients dont la glycémie dépasse 1.26 g/L
print("--- 5.2 Glycémie > 1.26 g/L ---");
const glycemiaHaut = db.analyses.aggregate([
  { $match: { type: "Glycémie", "resultats.valeur": { $gt: 1.26 } } },
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "patient_info"
    }
  },
  { $unwind: "$patient_info" },
  { $project: { "patient_info.nom": 1, "patient_info.prenom": 1, "resultats.valeur": 1 } }
]).toArray();
printjson(glycemiaHaut);

// 5.3 Statistiques croisées : taux d'analyses anormales par wilaya
// (On simule 'anormale' par valeur > 1.5)
print("--- 5.3 Taux d'analyses anormales (>1.5) par wilaya ---");
const statsWilaya = db.analyses.aggregate([
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "p"
    }
  },
  { $unwind: "$p" },
  { $group: {
      _id: "$p.adresse.wilaya",
      total_analyses: { $sum: 1 },
      anormales: { $sum: { $cond: [{ $gt: ["$resultats.valeur", 1.5] }, 1, 0] } }
  }},
  { $project: {
      wilaya: "$_id",
      taux_anormal: { $multiply: [{ $divide: ["$anormales", "$total_analyses"] }, 100] }
  }}
]).toArray();
printjson(statsWilaya);
