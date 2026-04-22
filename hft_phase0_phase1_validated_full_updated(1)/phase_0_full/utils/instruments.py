import requests
import pandas as pd
from io import StringIO  # ✅ FIXED

def get_fno_instruments():
    url = "https://api.kite.trade/instruments"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise Exception("Failed to fetch instruments list from Kite")

    # ✅ Use standard StringIO here
    df = pd.read_csv(StringIO(response.text))

    # Filter only F&O instruments
    df = df[(df["segment"] == "NFO-OPT") | (df["segment"] == "NFO-FUT")]

    df.to_csv("phase_0_full/utils/instruments_fno.csv", index=False)

    instrument_map = {row["tradingsymbol"]: int(row["instrument_token"]) for _, row in df.iterrows()}
    return instrument_map
