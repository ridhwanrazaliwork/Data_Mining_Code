# producer.py
import time
import json
import uuid
import random
from datetime import datetime
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

STREAM = "mystream"

def make_event():
    return {
        "id": str(uuid.uuid4()),
        "ts": datetime.utcnow().isoformat(),
        "event_type": random.choice(["beli", "lihat", "tambah_ke_troli", "daftar", "klik"]),
        "platform": random.choice(["Shopee", "Lazada", "Grab", "Website", "MySejahtera"]),
        "city": random.choice(["Kuala Lumpur", "George Town", "Johor Bahru", "Kota Kinabalu", "Kuching", "Ipoh", "Shah Alam"]),
        "amount_myr": f"{random.uniform(1, 500):.2f}"
    }

def run(interval=1.0):
    print("Producer started. Press Ctrl+C to stop.")
    try:
        while True:
            ev = make_event()
            # xadd requires a mapping of string keys->string values
            msg_id = r.xadd(STREAM, ev)
            print(f"Produced {msg_id} -> {json.dumps(ev)}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Producer stopped.")

if __name__ == "__main__":
    run()