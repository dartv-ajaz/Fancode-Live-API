import requests
import json
import os

SOURCE_URL = "https://raw.githubusercontent.com/drmlive/fancode-live-events/main/fancode.json"
FILE_NAME = "live_matches.json"

def fetch_drm_data():
    print("--- Step 1: Source Se Connect Ho Raha Hai ---")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print("✅ Connection Successful!")
            data = response.json()
            
            # --- CHANNELS COUNT KARNE KA LOGIC ---
            if isinstance(data, list):
                total_channels = len(data)
            elif isinstance(data, dict) and "matches" in data:
                total_channels = len(data["matches"])
            else:
                total_channels = "Unknown"
                
            print(f"📺 Total Channels/Matches Fetch Hue: {total_channels}")
            # -------------------------------------
            
            print("--- Step 2: File Create Ho Rahi Hai ---")
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            
            if os.path.exists(FILE_NAME):
                print(f"✅ SUCCESS! Data '{FILE_NAME}' mein save ho gaya hai.")
        else:
            print(f"❌ Error: Status Code {response.status_code}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    fetch_drm_data()
