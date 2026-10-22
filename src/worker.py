import json

import redis

from src.db import get_conn, save
from src.detector import ZScoreDetector


def main():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True,
                    socket_timeout=30, socket_connect_timeout=10)
    r.ping()
    conn = get_conn()
    detectors = {}
    processed = flagged = 0

    print("Worker started. Waiting for readings... (Ctrl+C to stop)")
    while True:
        try:
            item = r.brpop("readings", timeout=5)
        except redis.exceptions.TimeoutError:
            continue
        except KeyboardInterrupt:
            break
        if item is None:
            continue

        msg = json.loads(item[1])
        det = detectors.setdefault(msg["metric"], ZScoreDetector())
        z, is_anomaly, severity = det.score(msg["value"])
        processed += 1

        save(conn, msg["metric"], msg["timestamp"], msg["value"], z, is_anomaly, severity)
        if processed % 100 == 0:
            conn.commit()

        if is_anomaly:
            flagged += 1
            print(f"[ALERT {severity}] {msg['metric']} at {msg['timestamp']} "
                  f"value={msg['value']:.2f} z={z:.1f}")

        if processed % 500 == 0:
            print(f"-- processed {processed} readings, flagged {flagged}")

    conn.commit()
    conn.close()
    print(f"Stopped. Processed {processed}, flagged {flagged}.")


if __name__ == "__main__":
    main()