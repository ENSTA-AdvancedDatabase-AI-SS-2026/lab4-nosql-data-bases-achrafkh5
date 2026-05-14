use("medical_db");

db.patients.createIndex({ "adresse.wilaya": 1, antecedents: 1 });
db.patients.createIndex({ "consultations.date": 1 });
db.patients.createIndex({ "consultations.diagnostic": "text" });
db.analyses.createIndex({ patient_id: 1 });

const requeteTest = {
  "adresse.wilaya": "Alger",
  antecedents: "Diabète type 2"
};

const explainStats = db.patients.find(requeteTest).explain("executionStats");
printjson(explainStats.executionStats);

db.analyses.createIndex(
  { date: 1 },
  { expireAfterSeconds: 157680000 }
);

