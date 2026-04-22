import boto3
import json
from phase_0_full.utils.logger import log

# Kinesis Configuration
STREAM_NAME = "raw_ticks"         # Your Kinesis stream name
REGION = "ap-south-1"             # Your AWS region

# Create Kinesis client
client = boto3.client("kinesis", region_name=REGION)

def push_to_kinesis(data: dict):
    """
    Push a dictionary to AWS Kinesis Stream.
    """
    try:
        # Convert dict to JSON string
        payload = json.dumps(data)

        # Ensure PartitionKey is a string (Kinesis requires it)
        partition_key_raw = data.get("symbol", "unknown")
        partition_key = str(partition_key_raw)

        # Send record
        response = client.put_record(
            StreamName=STREAM_NAME,
            Data=payload,
            PartitionKey=partition_key
        )
        log(f"✅ Sent to Kinesis: {partition_key}")
        return response

    except Exception as e:
        log(f"❌ Failed to push to Kinesis: {e}")
        return None

# Example usage
if __name__ == "__main__":
    sample_data = {
        "symbol": "RELIANCE24MAY2600CE",
        "ltp": 23.35,
        "volume": 15000,
        "oi": 1450000,
        "iv": 0.25,
        "delta": 0.42,
        "gamma": 0.06,
        "vega": 0.15,
        "theta": -0.09,
        "timestamp": "2025-05-25T12:00:00.000Z"
    }
    push_to_kinesis(sample_data)
