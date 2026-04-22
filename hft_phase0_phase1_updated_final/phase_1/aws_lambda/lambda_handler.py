
import base64
import json
import boto3
from datetime import datetime

kinesis_client = boto3.client("kinesis")
OUTPUT_STREAM = "processed_signals"

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(base64.b64decode(record["kinesis"]["data"]).decode("utf-8"))

        try:
            ltp = payload["ltp"]
            oi = payload["oi"]
            iv = payload["iv"]
            delta = payload["delta"]
            timestamp = payload["timestamp"]
            symbol = payload["symbol"]

            confidence = round(min(1.0, max(0.3, (delta + iv) / 2)), 2)
            entry_price = ltp
            stop_loss = round(entry_price * 0.99, 2)
            target = round(entry_price * 1.01, 2)

            signal = {
                "symbol": symbol,
                "signal": "BUY" if delta > 0.4 else "SELL",
                "entry": entry_price,
                "stop_loss": stop_loss,
                "target": target,
                "confidence": confidence,
                "strategy": "VWAP_Breakout",
                "timestamp": timestamp
            }

            kinesis_client.put_record(
                StreamName=OUTPUT_STREAM,
                Data=json.dumps(signal),
                PartitionKey=symbol
            )
        except Exception as e:
            print("❌ Lambda processing error:", e)

    return {"status": "ok"}
