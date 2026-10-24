import argparse
import json
import os
import time

import pandas as pd
import redis


def main():
    parser = argparse.ArgumentParser(description="Replay a NAB metric as a live stream")
    parser.add_argument("--file", required=True, help="path to a NAB csv")
    parser.add_argument("--rate", type=float, default=20, help="readings per second")
    parser.add_argument("--limit", type=int, default=0, help="stop after N readings (0 = all)")
    args = parser.parse_args()

    r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379,
                    decode_responses=True)
    r.ping()

    df = pd.read_csv(args.file, parse_dates=["timestamp"])
    metric = args.file.replace("\\", "/").split("/")[-1].replace(".csv", "")
    if args.limit:
        df = df.head(args.limit)

    print(f"Streaming {len(df)} readings of {metric} at {args.rate}/sec")
    for row in df.itertuples(index=False):
        msg = {"metric": metric, "timestamp": str(row.timestamp), "value": float(row.value)}
        r.lpush("readings", json.dumps(msg))
        time.sleep(1 / args.rate)
    print("Done.")


if __name__ == "__main__":
    main()