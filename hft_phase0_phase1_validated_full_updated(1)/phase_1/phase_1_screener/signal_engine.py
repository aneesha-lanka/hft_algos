import pandas as pd
import numpy as np
import redis
import json
from datetime import datetime
from kiteconnect import KiteConnect

# --- Config ---
API_KEY = "mgiyg240coa7al5u"          # Replace with your actual API key
ACCESS_TOKEN = "n4l4t42nyo79nog95i4oefpokn95gaqt"  # Replace with your actual access token
CAPITAL = 100000  # ₹1L capital
SMA_SHORT = 20
SMA_LONG = 50
MIN_VOLUME = 10000

# --- Redis connection ---
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# --- Get live lot sizes from Kite Connect ---
def get_lot_sizes(api_key, access_token):
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)

    instruments = kite.instruments("NFO")
    df = pd.DataFrame(instruments)
    fno_df = df[df['segment'] == 'NFO-OPT']
    return dict(zip(fno_df['tradingsymbol'], fno_df['lot_size']))

# --- Get live ticks from Redis ---
def get_ticks():
    keys = redis_client.keys("tick:*")
    ticks = []
    for key in keys:
        try:
            raw = redis_client.get(key)
            data = json.loads(raw)
            ticks.append(data)
        except:
            continue
    return ticks

# --- Run the screener logic ---
def run_screener():
    ticks = get_ticks()
    if not ticks:
        return pd.DataFrame()

    df = pd.DataFrame(ticks)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
    df = df.dropna(subset=['last_price', 'timestamp'])

    lot_sizes = get_lot_sizes(API_KEY, ACCESS_TOKEN)
    results = []

    for symbol in df['tradable'].unique():
        df_s = df[df['tradable'] == symbol].sort_values("timestamp").copy()
        if len(df_s) < SMA_LONG:
            continue

        df_s['VWAP'] = (df_s['last_price'] * df_s['volume']).cumsum() / df_s['volume'].cumsum()
        df_s['SMA20'] = df_s['last_price'].rolling(SMA_SHORT).mean()
        df_s['SMA50'] = df_s['last_price'].rolling(SMA_LONG).mean()

        latest = df_s.iloc[-1]
        signal = None

        try:
            if latest['last_price'] > latest['VWAP'] and latest['volume'] > MIN_VOLUME:
                signal = 'VWAP Breakout'
            elif latest['SMA20'] > latest['SMA50']:
                signal = 'SMA Crossover'
            elif ('open_interest' in df_s and
                  df_s['open_interest'].iloc[-1] - df_s['open_interest'].iloc[-3] > 1000):
                signal = 'OI Spike'
            else:
                continue
        except:
            continue

        lot_size = lot_sizes.get(symbol, 1)
        entry = latest['last_price']
        lots = int(CAPITAL / (entry * lot_size))
        sl = round(entry * 0.98, 2)
        tp = round(entry * 1.02, 2)
        profit = lot_size * lots * (tp - entry)

        results.append({
            'Stock': symbol,
            'Signal': signal,
            'Entry': round(entry, 2),
            'SL': sl,
            'TP': tp,
            'Lots': lots,
            'Profit/Lot': round(profit, 2)
        })

    result_df = pd.DataFrame(results)
    result_df.to_csv("logs/screener_output.csv", index=False)
    return result_df

# --- Run the script ---
if __name__ == "__main__":
    df = run_screener()
    if df.empty:
        print("No valid trades.")
    else:
        print(df.to_string(index=False))
