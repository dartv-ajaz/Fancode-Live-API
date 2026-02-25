import requests
import json

# Source URL
SOURCE_URL = "https://raw.githubusercontent.com/byte-capsule/FanCode-Hls-Fetcher/main/data.json"
FILE_NAME = "live_matches.json"

def fetch_data():
    try:
        print("Fetching data from FanCode source...")
        response = requests.get(SOURCE_URL, timeout=20)
        response.raise_for_status()
        
        data = response.json()
        all_matches = data.get("matches", [])
        
        # 1. LIVE matches ko alag karein
        live_matches = [m for m in all_matches if str(m.get("status")).upper() == "LIVE"]
        
        # 2. UPCOMING matches ko alag karein (taake app khali na rahe)
        upcoming_matches = [m for m in all_matches if str(m.get("status")).upper() == "UPCOMING"]
        
        # Final list: Pehle LIVE dikhayein, phir UPCOMING
        final_list = live_matches + upcoming_matches
        
        output = {
            "success": True,
            "status": "Online",
            "last_update": data.get("last update time"),
            "live_count": len(live_matches),
            "upcoming_count": len(upcoming_matches),
            "matches": final_list
        }
        
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
            
        print(f"✅ Done! Found {len(live_matches)} Live and {len(upcoming_matches)} Upcoming matches.")
        print(f"📂 File saved as {FILE_NAME}")

    except Exception as e:
        print(f"❌ Error logic mein hai: {e}")

if __name__ == "__main__":
    fetch_data()
