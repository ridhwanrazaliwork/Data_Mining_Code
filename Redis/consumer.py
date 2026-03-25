# consumer.py
import time
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

STREAM = "mystream"
GROUP = "mygroup"
CONSUMER = "consumer-1"
BLOCK_MS = 5000

def ensure_group():
    try:
        # create group with start id '0' (safe if stream exists or mkstream=True)
        r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
        print("Consumer group created.")
    except redis.exceptions.ResponseError as e:
        # group already exists
        if "BUSYGROUP" in str(e):
            print("Consumer group already exists.")
        else:
            raise

def run():
    ensure_group()
    print("Consumer started. Waiting for new messages...")
    try:
        while True:
            entries = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=BLOCK_MS)
            if not entries:
                continue
            for stream_name, messages in entries:
                for msg_id, data in messages:
                    print(f"Consumed {msg_id} -> {data}")
                    # ACK the message after processing
                    r.xack(STREAM, GROUP, msg_id)
    except KeyboardInterrupt:
        print("Consumer stopped.")

if __name__ == "__main__":
    run()