
import boto3
import json
import time

STREAM_NAME = "processed_signals"
REGION = "ap-south-1"

client = boto3.client("kinesis", region_name=REGION)
shard_id = client.describe_stream(StreamName=STREAM_NAME)['StreamDescription']['Shards'][0]['ShardId']
shard_iterator = client.get_shard_iterator(
    StreamName=STREAM_NAME,
    ShardId=shard_id,
    ShardIteratorType="LATEST"
)["ShardIterator"]

print("📡 Listening to enriched signals from processed_signals stream...")

while True:
    out = client.get_records(ShardIterator=shard_iterator, Limit=10)
    shard_iterator = out["NextShardIterator"]

    for rec in out["Records"]:
        signal = json.loads(rec["Data"])
        print("🔔 New Trade Signal:")
        print(json.dumps(signal, indent=2))

    time.sleep(1)
