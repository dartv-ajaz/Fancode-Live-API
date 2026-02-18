import requests
import json
from datetime import datetime
import pytz

def get_hotstar():
    url = "https://api.hotstar.com/o/v1/page/1558?app_version=9.15.0"
    headers = {
        "x-hs-platform": "android",
        "User-Agent": "Hotstar;in.startv.hotstar/9.15.0 (Android/10)"
    }
    matches = []
    try:
        res = requests.get(url, headers=headers).json()
        items = res.get("body", {}).get("results", {}).get("items", [])
        allowed = ['cricket', 'hockey', 'kabaddi']
        for item in items:
            title = item.get("title", "").lower()
            if any(s in title for s in allowed):
                matches.append({
                    "title": item.get("title"),
                    "url": f"https://www.hotstar.com/{item.get('contentId')}",
                    "license_url": "https://license.drm.hotstar.com/widevine/v1/play",
                    "platform": "Hotstar",
                    "type": "DRM"
                })
    except: pass
    return matches

def main():
    all_matches = get_hotstar() # Prime logic can be added here
    output = {
        "last_updated": datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M %p"),
        "matches": all_matches
    }
    with open('live_matches_B.json', 'w') as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    main()
