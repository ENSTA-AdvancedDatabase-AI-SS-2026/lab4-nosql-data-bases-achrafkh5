use("medical_db");

const diagParWilaya = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: { 
      _id: { wilaya: "$adresse.wilaya", diagnostic: "$consultations.diagnostic" }, 
      count: { $sum: 1 } 
    } 
  },
  { $sort: { count: -1 } },
  { $limit: 20 }
]).toArray();
printjson(diagParWilaya);

const medsParSpecialite = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $unwind: "$consultations.medicaments" },
  { $group: { 
      _id: { specialite: "$consultations.medecin.specialite", medicament: "$consultations.medicaments.nom" }, 
      count: { $sum: 1 } 
    } 
  },
  { $sort: { count: -1 } },
  { $group: { 
      _id: "$_id.specialite", 
      top_med: { $first: "$_id.medicament" }, 
      count: { $first: "$count" } 
    } 
  }
]).toArray();
printjson(medsParSpecialite);

const evolutionMensuelle = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $match: {
    "consultations.date": {
      $gte: new Date(new Date().setFullYear(new Date().getFullYear() - 1))
    }
  }},
  { $group: { 
      _id: { 
        year: { $year: "$consultations.date" }, 
        month: { $month: "$consultations.date" } 
      }, 
      count: { $sum: 1 } 
    } 
  },
  { $sort: { "_id.year": 1, "_id.month": 1 } },
  { $project: { 
      date: { $concat: [{ $toString: "$_id.year" }, "-", { $toString: "$_id.month" }] }, 
      count: 1, 
      _id: 0 
    } 
  }
]).toArray();
printjson(evolutionMensuelle);

const patientsRisque = db.patients.aggregate([
  {
    $match: {
      antecedents: { $all: ["Diabète type 2", "HTA"] },
      dateNaissance: { $lt: new Date(new Date().setFullYear(new Date().getFullYear() - 60)) }
    }
  },
  { $addFields: {
      age: { $subtract: [new Date().getFullYear(), { $year: "$dateNaissance" }] },
      nb_consultations: { $size: "$consultations" }
    }
  },
  { $group: {
      _id: null,
      avg_age: { $avg: "$age" },
      total_patients: { $sum: 1 }
    }
  }
]).toArray();
printjson(patientsRisque);

const rapportMedecins = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: {
      _id: "$consultations.medecin.nom",
      patients_uniques: { $addToSet: "$_id" },
      total_consultations: { $sum: 1 }
    }
  },
  { $addFields: {
      nb_uniques: { $size: "$patients_uniques" },
      taux_reconsultation: {
        $multiply: [
          { $divide: [{ $subtract: ["$total_consultations", { $size: { $ifNull: ["$patients_uniques", []] } }] }, { $size: { $ifNull: ["$patients_uniques", [1]] } }] },
          100
        ]
      }
    }
  },
  { $sort: { total_consultations: -1 } },
  { $limit: 5 }
]).toArray();
printjson(rapportMedecins);

