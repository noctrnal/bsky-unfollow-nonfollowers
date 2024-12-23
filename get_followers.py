import os
import requests
from bluesky_auth import BlueskyAuth
import json

class BlueskyFollowers:
    def __init__(self):
        self.auth = BlueskyAuth()
        self.headers = self.auth.get_auth_header()
        self.base_url = "https://bsky.social/xrpc"
    
    def get_followers(self, handle, limit=100):
        """
        Fetch all followers for a given Bluesky handle.
        
        Args:
            handle (str): Bluesky handle (e.g., "@username.bsky.social")
            limit (int): Number of results per page
            
        Returns:
            list: List of follower information dictionaries
        """
        followers = []
        cursor = None
        
        while True:
            # Construct URL with parameters
            url = f"{self.base_url}/app.bsky.graph.getFollowers"
            params = {"actor": handle, "limit": limit}
            if cursor:
                params["cursor"] = cursor
            
            # Make the request
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error fetching followers: {response.status_code}")
                print(response.text)
                break
                
            data = response.json()
            followers.extend(data.get("followers", []))
            
            # Check if there are more pages
            cursor = data.get("cursor")
            if not cursor:
                break
        
        return followers

    def save_followers_to_file(self, handle, filename="followers.json"):
        """
        Fetch followers and save them to a JSON file.
        
        Args:
            handle (str): Bluesky handle
            filename (str): Output JSON filename
        """
        followers = self.get_followers(handle)
        
        # Extract relevant information
        follower_data = [{
            "did": follower["did"],
            "handle": follower["handle"],
            "displayName": follower.get("displayName", "")
        } for follower in followers]
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(follower_data, f, indent=2)
        
        print(f"Saved {len(follower_data)} followers to {filename}")

def main():
    bf = BlueskyFollowers()
    handle = os.getenv("BLUESKY_HANDLE")
    bf.save_followers_to_file(handle)

if __name__ == "__main__":
    main() 