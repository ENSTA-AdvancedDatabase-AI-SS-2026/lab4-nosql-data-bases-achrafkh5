import time
import statistics
import json
import redis
from pymongo import MongoClient

def measure_latency(fn, iterations=100):
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        latencies.append((time.perf_counter() - start) * 1000)
    latencies.sort()
    return {
        "mean_ms": statistics.mean(latencies),
        "p50_ms": latencies[int(0.50 * len(latencies))],
        "p95_ms": latencies[int(0.95 * len(latencies))],
        "throughput_rps": 1000 / (statistics.mean(latencies) if statistics.mean(latencies) > 0 else 1)
    }

def benchmark_write_redis(n=10000):
    r = redis.Redis(host='localhost', port=6379)
    r.flushdb()
    start = time.time()
    pipe = r.pipeline()
    for i in range(n):
        pipe.set(f"key:{i}", f"value:{i}")
        if i % 1000 == 0:
            pipe.execute()
    pipe.execute()
    elapsed = time.time() - start
    print(f"Redis Write: {n/elapsed:.2f} ops/s")

def benchmark_write_mongodb(n=10000):
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["benchmark"]
    col = db["test"]
    col.delete_many({})
    start = time.time()
    batch_size = 1000
    for i in range(0, n, batch_size):
        docs = [{"key": j, "val": j} for j in range(i, min(i + batch_size, n))]
        col.insert_many(docs)
    elapsed = time.time() - start
    print(f"MongoDB Write: {n/elapsed:.2f} ops/s")

if __name__ == "__main__":
    N = 10000
    benchmark_write_redis(N)
    benchmark_write_mongodb(N)
