import boto3
import json

# Create Kinesis client
client = boto3.client("kinesis", region_name="ap-south-1")  # Replace if needed

# Describe stream and get first shard
response = client.describe_stream(StreamName="raw_ticks")
shard_id = response['StreamDescription']['Shards'][0]['ShardId']

# Get shard iterator from beginning
shard_iterator = client.get_shard_iterator(
    StreamName="raw_ticks",
    ShardId=shard_id,
    ShardIteratorType="TRIM_HORIZON"  # fetch from the start
)['ShardIterator']

# Fetch records
records_response = client.get_records(ShardIterator=shard_iterator, Limit=10)

records = records_response['Records']

if not records:
    print("❌ No records found in Kinesis stream.")
else:
    print(f"✅ Found {len(records)} records:\n")
    for record in records:
        try:
            data = json.loads(record['Data'].decode("utf-8"))
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"⚠️ Error decoding record: {e}")
