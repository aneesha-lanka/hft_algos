import boto3
import json
import time

STREAM_NAME = "raw_ticks"
REGION = "ap-south-1"

client = boto3.client("kinesis", region_name=REGION)

def read_kinesis_records():
    response = client.describe_stream(StreamName=STREAM_NAME)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']

    iterator = client.get_shard_iterator(
        StreamName=STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType='LATEST'
    )['ShardIterator']

    print(f"📥 Listening to stream '{STREAM_NAME}'...")

    while True:
        output = client.get_records(ShardIterator=iterator, Limit=5)
        records = output['Records']
        iterator = output['NextShardIterator']

        for record in records:
            data = record['Data'].decode('utf-8')
            print("🧾", json.loads(data))

        time.sleep(2)

if __name__ == "__main__":
    read_kinesis_records()
