import requests
import json
from datetime import datetime
import pytz

def get_fancode():
    url = "https://www.fancode.com/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    payload = {
        "query": """query LiveEvents { events(status: LIVE) { edges { node { id name category { name } teams { name } media { streamLinks { hls } } } } } }"""
    }
    matches = []
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        edges = res.get("data", {}).get("events", {}).get("edges", [])
        allowed = ['cricket', 'hockey', 'kabaddi']
        for edge in edges:
            node = edge.get("node", {})
            cat = node.get("category", {}).get("name", "").lower()
            if cat in allowed:
                matches.append({
                    "title": node.get("name"),
                    "url": node.get("media", [])[0]["streamLinks"]["hls"],
                    "platform": "FanCode",
                    "sport": cat,
                    "type": "HLS"
                })
    except: pass
    return matches

def get_jio():
    # JioCinema Prototype logic
    return [{"title": "Jio Live Match", "url": "JIO_STREAM_URL", "platform": "JioCinema", "sport": "cricket", "type": "HLS"}]

def main():
    all_matches = get_fancode() + get_jio()
    output = {
        "last_updated": datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M %p"),
        "matches": all_matches
    }
    with open('live_matches_A.json', 'w') as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    main()
