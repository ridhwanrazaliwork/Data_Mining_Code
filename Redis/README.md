
# Redis Streams demo — producer & consumer

What this does
- Simple demo of Redis Streams: a Python producer that writes Malaysia-themed events and a Python consumer that reads + ACKs via a consumer group.
- Intended for local testing on WSL2; inspect stream contents with `redis-cli`.

Prerequisites
- Redis server running on WSL2 (example: `redis-server --daemonize yes`)
- Python 3 and the `redis` client: `pip install redis`

Files
- producer: `producer.py` — produces events to stream `mystream`
- consumer: `consumer.py` — consumes from consumer group `mygroup` and ACKs messages

Quick start (WSL2)
```bash
# start Redis (example)
redis-server --daemonize yes

# install python client
pip install redis

# run producer (new terminal)
python producer.py

# run consumer (another terminal)
python consumer.py
```

Produce 50 events quickly (one-off)
```bash
python -c "from producer import run; run(0.01)"  # press Ctrl+C after ~0.5s to stop or adapt
```

Useful redis-cli commands (limit output to 5)
```bash
# show first 5 entries
redis-cli XRANGE mystream - + COUNT 5

# show newest 5 entries
redis-cli XREVRANGE mystream + - COUNT 5

# stream summary (length, first/last IDs)
redis-cli XINFO STREAM mystream

# list consumer groups (pipe to head if long)
redis-cli XINFO GROUPS mystream | head -n 20

# inspect pending messages
redis-cli XPENDING mystream mygroup
```

Notes & tips
- Producer uses `XADD` to append events. Values are stored as strings.
- Consumer uses `XGROUP`/`XREADGROUP` + `XACK`; the demo creates the group if missing.
- To replay from the beginning, recreate the consumer group with `id 0` (or use `XREAD`/`XRANGE`).
- To simulate multiple consumers, run `consumer.py` with a different `CONSUMER` name or duplicate the file.
- Use `XCLAIM` and `XPENDING` to inspect and recover stuck messages if a consumer crashes.
