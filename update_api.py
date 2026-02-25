import requests
import json

# Source URL jahan se data lana hai
SOURCE_URL = "https://raw.githubusercontent.com/byte-capsule/FanCode-Hls-Fetcher/main/data.json"
FILE_NAME = "live_matches.json"

def fetch_and_save():
    try:
        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            data = response.json()
            # Sirf 'LIVE' matches filter karne ke liye (taki API clean rahe)
            live_only = [m for m in data.get("matches", []) if m.get("status") == "LIVE"]
            
            output = {
                "success": True,
                "last_update": data.get("last update time"),
                "matches": live_only
            }
            
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4)
            print("✅ Data updated successfully!")
        else:
            print("❌ Source se data nahi mila.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_save()
