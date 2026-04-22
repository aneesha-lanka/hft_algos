
import boto3

def check_aws_credentials():
    try:
        client = boto3.client("sts")
        identity = client.get_caller_identity()
        print("✅ AWS Credentials Valid!")
        print("User ID:", identity['UserId'])
        print("Account:", identity['Account'])
        print("ARN:", identity['Arn'])
    except Exception as e:
        print("❌ AWS Credential check failed:", e)

if __name__ == "__main__":
    check_aws_credentials()
