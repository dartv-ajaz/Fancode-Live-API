import requests
import json
from datetime import datetime
import pytz

def fetch_live_matches():
    print("Fetching data from FanCode...")
    
    # FanCode GraphQL API URL
    url = "https://www.fancode.com/graphql"
    
    # Headers to bypass basic bot-protection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.fancode.com",
        "Referer": "https://www.fancode.com/"
    }

    # GraphQL payload for live events
    payload = {
        "query": """
        query LiveEvents {
            events(status: LIVE) {
                edges {
                    node {
                        id
                        name
                        category { name }
                        teams { name, contentInfo { flag } }
                        media { streamLinks { hls } }
                    }
                }
            }
        }
        """
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # Humari app ka format
        api_data = {
            "type": "FanCode Auto Live API",
            "last_updated": datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %I:%M:%S %p"),
            "matches": []
        }

        # Data ko extract karke apne format mein dalna
        edges = data.get("data", {}).get("events", {}).get("edges", [])
        for edge in edges:
            match = edge.get("node", {})
            teams = match.get("teams", [])
            media = match.get("media", [])
            
            if len(teams) >= 2 and media and media[0].get("streamLinks", {}).get("hls"):
                team1 = teams[0]
                team2 = teams[1]
                
                api_data["matches"].append({
                    "match_id": match.get("id"),
                    "event_catagory": match.get("category", {}).get("name", "sports").lower(),
                    "event_name": match.get("name"),
                    "team_1": team1.get("name"),
                    "team_1_flag": team1.get("contentInfo", {}).get("flag", ""),
                    "team_2": team2.get("name"),
                    "team_2_flag": team2.get("contentInfo", {}).get("flag", ""),
                    "stream_link": media[0]["streamLinks"]["hls"]
                })

        # File save karna
        with open('live_matches.json', 'w') as f:
            json.dump(api_data, f, indent=4)
            
        print(f"Successfully saved {len(api_data['matches'])} matches!")

    except Exception as e:
        print("Error fetching data:", e)

if __name__ == "__main__":
    fetch_live_matches()
