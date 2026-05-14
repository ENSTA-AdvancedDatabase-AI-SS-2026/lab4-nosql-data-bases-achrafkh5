import sys
from unittest.mock import MagicMock
sys.modules["asyncore"] = MagicMock()
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType
import uuid
import random
from datetime import datetime, timedelta
import time

CASSANDRA_HOST = 'localhost'
KEYSPACE = 'smartgrid'
NB_CAPTEURS = 1000
MINUTES_HISTORIQUE = 5

WILAYAS = ["Alger", "Oran", "Constantine", "Annaba", "Blida"]
COMMUNES = {
    "Alger": ["Bab Ezzouar", "Hydra", "El Harrach", "Dar El Beida"],
    "Oran": ["Bir El Djir", "Es Senia", "Arzew"],
    "Constantine": ["El Khroub", "Ain Smara", "Hamma Bouziane"],
    "Annaba": ["El Bouni", "El Hadjar", "Seraidi"],
    "Blida": ["Bougara", "Boufarik", "Larbaa"],
}

from cassandra.io.asyncioreactor import AsyncioConnection

def connect():
    cluster = Cluster([CASSANDRA_HOST], connection_class=AsyncioConnection)
    session = cluster.connect(KEYSPACE)
    return session, cluster

def generate_mesure(capteur_id, wilaya, commune, timestamp):
    tension_base = 220
    return {
        "capteur_id": capteur_id,
        "date_jour": timestamp.date(),
        "timestamp": timestamp,
        "wilaya": wilaya,
        "commune": commune,
        "tension_v": round(tension_base + random.gauss(0, 5), 2),
        "courant_a": round(random.uniform(0.5, 15.0), 2),
        "puissance_kw": round(random.uniform(0.1, 3.3), 3),
        "frequence_hz": round(50 + random.gauss(0, 0.1), 2),
        "temperature": round(random.uniform(20, 65), 1),
        "alerte": random.random() < 0.05,
    }

def insert_single(session, mesure):
    query = "INSERT INTO mesures_par_capteur (capteur_id, date_jour, timestamp, wilaya, commune, tension_v, courant_a, puissance_kw, frequence_hz, temperature, alerte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    prepared = session.prepare(query)
    session.execute(prepared, (mesure["capteur_id"], mesure["date_jour"], mesure["timestamp"], mesure["wilaya"], mesure["commune"], mesure["tension_v"], mesure["courant_a"], mesure["puissance_kw"], mesure["frequence_hz"], mesure["temperature"], mesure["alerte"]))

def insert_batch(session, mesures: list):
    query = "INSERT INTO mesures_par_capteur (capteur_id, date_jour, timestamp, wilaya, commune, tension_v, courant_a, puissance_kw, frequence_hz, temperature, alerte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    prepared = session.prepare(query)
    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    for m in mesures:
        batch.add(prepared, (m["capteur_id"], m["date_jour"], m["timestamp"], m["wilaya"], m["commune"], m["tension_v"], m["courant_a"], m["puissance_kw"], m["frequence_hz"], m["temperature"], m["alerte"]))
    session.execute(batch)

def run_ingestion(session):
    start = time.time()
    capteurs = []
    for _ in range(NB_CAPTEURS):
        w = random.choice(WILAYAS)
        c = random.choice(COMMUNES[w])
        capteurs.append((uuid.uuid4(), w, c))
    total_inserted = 0
    now = datetime.now()
    for i in range(MINUTES_HISTORIQUE):
        ts = now - timedelta(minutes=i)
        mesures = []
        for cid, w, c in capteurs:
            m = generate_mesure(cid, w, c, ts)
            mesures.append(m)
            if len(mesures) >= 50:
                insert_batch(session, mesures)
                total_inserted += len(mesures)
                mesures = []
        if mesures:
            insert_batch(session, mesures)
            total_inserted += len(mesures)
    elapsed = time.time() - start
    print(f"✅ {total_inserted} mesures insérées en {elapsed:.1f}s")
    print(f"   Débit : {total_inserted/elapsed:,.0f} m/s")

if __name__ == "__main__":
    session, cluster = connect()
    run_ingestion(session)
    cluster.shutdown()

