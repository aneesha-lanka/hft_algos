
import boto3
import json

def check_stream_exists(stream_name):
    client = boto3.client("kinesis")
    try:
        response = client.describe_stream(StreamName=stream_name)
        status = response['StreamDescription']['StreamStatus']
        print(f"✅ Stream '{stream_name}' exists. Status: {status}")
    except client.exceptions.ResourceNotFoundException:
        print(f"❌ Stream '{stream_name}' does NOT exist.")
    except Exception as e:
        print(f"❌ Error checking stream '{stream_name}':", e)

def check_lambda(lambda_name):
    client = boto3.client("lambda")
    try:
        response = client.get_function(FunctionName=lambda_name)
        print(f"✅ Lambda function '{lambda_name}' exists.")
        role = response['Configuration']['Role']
        print(f"🔐 Lambda role: {role}")
    except client.exceptions.ResourceNotFoundException:
        print(f"❌ Lambda function '{lambda_name}' does NOT exist.")
    except Exception as e:
        print(f"❌ Error checking Lambda function '{lambda_name}':", e)

def check_lambda_trigger(lambda_name, expected_stream):
    client = boto3.client("lambda")
    try:
        response = client.list_event_source_mappings(FunctionName=lambda_name)
        found = False
        for mapping in response["EventSourceMappings"]:
            if expected_stream in mapping["EventSourceArn"]:
                found = True
                print(f"✅ Lambda is correctly triggered by '{expected_stream}' stream.")
                break
        if not found:
            print(f"❌ Lambda is NOT connected to stream '{expected_stream}'.")
    except Exception as e:
        print(f"❌ Error checking Lambda trigger:", e)

if __name__ == "__main__":
    print("🔍 Checking AWS HFT Pipeline Setup...\n")
    check_stream_exists("raw_ticks")
    check_stream_exists("processed_signals")
    check_lambda("hft_process_ticks")
    check_lambda_trigger("hft_process_ticks", "raw_ticks")
