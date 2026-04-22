
from kiteconnect import KiteTicker, KiteConnect
import json
import time
import os
import sys

# Add base path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from phase_0_full.kinesis.stream_producer import push_to_kinesis
from phase_0_full.utils.logger import log

# Load credentials
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "credentials_kite.json"))
with open(config_path) as f:
    creds = json.load(f)

API_KEY = creds["api_key"]
ACCESS_TOKEN = creds["access_token"]

# Initialize KiteConnect for token-name mapping
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

print("🔄 Fetching instrument tokens from Kite...")
instruments = kite.instruments("NSE")
token_map = {inst["instrument_token"]: inst["tradingsymbol"] for inst in instruments}

# You can also merge F&O if needed:
# instruments += kite.instruments("NFO")

# Define run control
THROTTLE_INTERVAL = 2  # seconds
MAX_RUNTIME = 300  # seconds
last_sent = {}
start_time = time.time()

def start_kite_stream(subscribe_tokens):
    kws = KiteTicker(API_KEY, ACCESS_TOKEN)

    def on_ticks(ws, ticks):
        current_time = time.time()

        for tick in ticks:
            token = tick.get("instrument_token")
            if not token:
                continue

            if current_time - last_sent.get(token, 0) >= THROTTLE_INTERVAL:
                symbol = token_map.get(token, f"TOKEN_{token}")

                data = {
                    "symbol": symbol,
                    "token": token,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
                    "ltp": tick.get("last_price"),
                    "volume": tick.get("volume_traded", 0),
                    "oi": tick.get("oi", 0)
                }

                push_to_kinesis(data)
                last_sent[token] = current_time

    def on_connect(ws, response):
        log("✅ WebSocket connected. Subscribing to tokens...")
        token_list = list(token_map.keys())[:100]  # Limit to 100 for stability
        ws.subscribe(token_list)

    def on_close(ws, code, reason):
        log(f"⚠️ WebSocket closed: {code} - {reason}")

    def on_error(ws, code, reason):
        log(f"❌ WebSocket error: {reason}")

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.on_error = on_error

    kws.connect(threaded=True)

    while True:
        if time.time() - start_time > MAX_RUNTIME:
            log("🛑 Max runtime reached. Closing WebSocket.")
            kws.close()
            break
        time.sleep(1)

if __name__ == "__main__":
    start_kite_stream(token_map)
