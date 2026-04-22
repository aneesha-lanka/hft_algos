# Placeholder for stream_consumer.py
import boto3
import json
import time

STREAM_NAME = "raw_ticks"  # Your source stream name
REGION = "ap-south-1"  # Your AWS region

# Initialize Kinesis client
client = boto3.client("kinesis", region_name=REGION)


def consume_raw_ticks():
    print(f"📡 Connecting to stream: {STREAM_NAME} in {REGION}")

    # Get shard ID
    response = client.describe_stream(StreamName=STREAM_NAME)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']

    # Get shard iterator
    shard_iterator = client.get_shard_iterator(
        StreamName=STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType="LATEST"
    )['ShardIterator']

    print("🔄 Listening for incoming tick data...")
    while True:
        out = client.get_records(ShardIterator=shard_iterator, Limit=100)
        shard_iterator = out['NextShardIterator']

        for record in out['Records']:
            try:
                tick_data = json.loads(record['Data'])
                print("🟢 Tick Received:")
                print(json.dumps(tick_data, indent=2))
                # Optional: Write to MongoDB, CSV, Redis etc.
            except Exception as e:
                print(f"❌ Error parsing record: {e}")

        time.sleep(1)


if __name__ == "__main__":
    consume_raw_ticks()
