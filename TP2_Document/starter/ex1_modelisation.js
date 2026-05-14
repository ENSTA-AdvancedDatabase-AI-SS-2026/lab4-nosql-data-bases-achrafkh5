use("medical_db");

db.patients.drop();
db.analyses.drop();

db.createCollection("patients", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cin", "nom", "prenom", "dateNaissance", "sexe"],
      properties: {
        cin: { bsonType: "string" },
        nom: { bsonType: "string" },
        prenom: { bsonType: "string" },
        dateNaissance: { bsonType: "date" },
        sexe: { enum: ["M", "F"] },
        adresse: {
          bsonType: "object",
          required: ["wilaya"],
          properties: {
            wilaya: { bsonType: "string" },
            commune: { bsonType: "string" }
          }
        }
      }
    }
  }
});

const patients = [];
const wilayas = ["Alger", "Oran", "Constantine", "Annaba", "Blida"];
const noms = ["Bensalem", "Ouali", "Mansouri", "Kaci", "Hadj"];
const prenoms = ["Ahmed", "Fatima", "Mohamed", "Amine", "Sonia"];
const pathologies = ["Diabète type 2", "HTA", "Asthme", "Anémie"];

for (let i = 0; i < 20; i++) {
  patients.push({
    cin: "1980" + Math.floor(Math.random() * 100000000),
    nom: noms[i % noms.length],
    prenom: prenoms[i % prenoms.length],
    dateNaissance: new Date(1960 + Math.floor(Math.random() * 40), 0, 1),
    sexe: i % 2 === 0 ? "M" : "F",
    adresse: { 
      wilaya: wilayas[i % wilayas.length], 
      commune: "Commune_" + i 
    },
    groupeSanguin: "O+",
    antecedents: [pathologies[i % pathologies.length]],
    consultations: [
      {
        id: UUID(),
        date: new Date("2024-01-15"),
        medecin: { nom: "Dr. Mansouri", specialite: "Cardiologie" },
        diagnostic: "Hypertension artérielle",
        tension: { systolique: 145, diastolique: 92 },
        medicaments: [{ nom: "Amlodipine", dosage: "5mg", duree: "30 jours" }],
        notes: "Suivi mensuel"
      },
      {
        id: UUID(),
        date: new Date("2024-03-20"),
        medecin: { nom: "Dr. Kaci", specialite: "Généraliste" },
        diagnostic: "Grippe",
        medicaments: [{ nom: "Paracétamol", dosage: "1g", duree: "5 jours" }]
      }
    ]
  });
}

db.patients.insertMany(patients);

const insertedPatients = db.patients.find().toArray();
const analyses = [];
const typesAnalyse = ["Glycémie", "NFS", "Lipidogramme", "Créatinine", "ECG"];

insertedPatients.forEach(p => {
  analyses.push({
    patient_id: p._id,
    date: new Date(),
    type: typesAnalyse[Math.floor(Math.random() * typesAnalyse.length)],
    resultats: { valeur: Math.random() * 2 },
    laboratoire: "Labo Central Alger",
    valide: true
  });
});

db.analyses.insertMany(analyses);

print("Patients:", db.patients.countDocuments());
print("Analyses:", db.analyses.countDocuments());

