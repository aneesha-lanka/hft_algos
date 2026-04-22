import os
import json
import webbrowser
from kiteconnect import KiteConnect

def main():
    print("\n🔐 Kite Access Token Generator\n")

    API_KEY = input("👉 Enter your Kite API Key: ").strip()
    API_SECRET = input("👉 Enter your Kite API Secret: ").strip()

    kite = KiteConnect(api_key=API_KEY)
    login_url = kite.login_url()

    print("\n🔗 Open this URL in your browser to login and get the request token:")
    print(login_url)
    webbrowser.open(login_url)

    request_token = input("\n🔑 Paste the request_token here: ").strip()

    try:
        data = kite.generate_session(request_token=request_token, api_secret=API_SECRET)
        access_token = data["access_token"]

        creds = {
            "api_key": API_KEY,
            "access_token": access_token
        }

        # Ensure path exists
        output_dir = os.path.join(os.path.dirname(__file__), "..", "config")
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, "credentials_kite.json"), "w") as f:
            json.dump(creds, f, indent=4)

        print("\n✅ Access token saved to: config/credentials_kite.json")

    except Exception as e:
        print(f"\n❌ Error generating access token: {e}")

# Allow standalone execution
if __name__ == "__main__":
    main()
