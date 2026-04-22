
from phase_0_full.utils.generate_access_token import main as generate_token
from phase_0_full.utils.instruments import get_fno_instruments
from phase_0_full.data_ingestion.kite_ws_producer import start_kite_stream


if __name__ == "__main__":
    print("🔐 Step 1: Ensure Access Token is Ready")
    generate_token()

    print("📦 Step 2: Fetch F&O instruments")
    instruments = get_fno_instruments()
    print(f"Loaded {len(instruments)} instruments")

    print("📡 Step 3: Starting Kite WebSocket Stream...")
    start_kite_stream(instruments)
