
import requests
import json
import datetime
from phase_0_full.data_ingestion.greeks_calculator import compute_greeks
from phase_0_full.utils.logger import log

with open("config/credentials_kite.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]
ACCESS_TOKEN = creds["access_token"]

HEADERS = {
    "X-Kite-Version": "3",
    "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}"
}

KITE_OPTION_CHAIN_URL = "https://api.kite.trade/instruments"

def fetch_option_chain(symbol):
    try:
        response = requests.get(KITE_OPTION_CHAIN_URL, headers=HEADERS)
        response.raise_for_status()
        all_instruments = response.text

        data = []
        for line in all_instruments.splitlines():
            if symbol in line and "NFO-OPT" in line:
                parts = line.split(",")
                try:
                    record = {
                        "tradingsymbol": parts[2],
                        "instrument_token": int(parts[0]),
                        "strike": float(parts[11]),
                        "expiry": parts[10],
                        "lot_size": int(parts[6]),
                        "option_type": parts[4],
                        "segment": parts[3],
                        "exchange": parts[9],
                        "tick_size": float(parts[8])
                    }
                    data.append(record)
                except Exception as e:
                    log(f"Parse error in line: {line}, error: {e}")

        return data

    except Exception as e:
        log(f"❌ Failed to fetch option chain: {e}")
        return []

def enrich_with_greeks(option_data, underlying_price, days_to_expiry):
    enriched = []
    for opt in option_data:
        # Mock values or default if Greeks missing
        greeks = compute_greeks(
            S=underlying_price,
            K=opt["strike"],
            T=days_to_expiry,
            r=0.06,
            sigma=0.25,  # fallback IV
            option_type=opt["option_type"]
        )
        opt.update(greeks)
        enriched.append(opt)
    return enriched

if __name__ == "__main__":
    symbol = "RELIANCE"
    option_chain = fetch_option_chain(symbol)
    print(f"✅ Retrieved {len(option_chain)} options for {symbol}")
