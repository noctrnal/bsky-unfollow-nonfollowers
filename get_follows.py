import os
import requests
from bluesky_auth import BlueskyAuth
import json

class BlueskyFollows:
    def __init__(self):
        self.auth = BlueskyAuth()
        self.headers = self.auth.get_auth_header()
        self.base_url = "https://bsky.social/xrpc"
    
    def get_follows(self, handle, limit=100):
        """
        Fetch all accounts that a given Bluesky handle follows.
        
        Args:
            handle (str): Bluesky handle (e.g., "@username.bsky.social")
            limit (int): Number of results per page
            
        Returns:
            list: List of follow information dictionaries
        """
        follows = []
        cursor = None
        
        while True:
            # Construct URL with parameters
            url = f"{self.base_url}/app.bsky.graph.getFollows"
            params = {"actor": handle, "limit": limit}
            if cursor:
                params["cursor"] = cursor
            
            # Make the request
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error fetching follows: {response.status_code}")
                print(response.text)
                break
                
            data = response.json()
            follows.extend(data.get("follows", []))
            
            # Check if there are more pages
            cursor = data.get("cursor")
            if not cursor:
                break
        
        return follows

    def save_follows_to_file(self, handle, filename="follows.json"):
        """
        Fetch follows and save them to a JSON file.
        
        Args:
            handle (str): Bluesky handle
            filename (str): Output JSON filename
        """
        follows = self.get_follows(handle)
        
        # Extract relevant information
        follow_data = [{
            "did": follow["did"],
            "handle": follow["handle"],
            "displayName": follow.get("displayName", "")
        } for follow in follows]
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(follow_data, f, indent=2)
        
        print(f"Saved {len(follow_data)} follows to {filename}")

def main():
    bf = BlueskyFollows()
    handle = os.getenv("BLUESKY_HANDLE")
    bf.save_follows_to_file(handle)

if __name__ == "__main__":
    main() 