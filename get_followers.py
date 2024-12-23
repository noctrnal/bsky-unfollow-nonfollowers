from typing import List, Dict, Optional
import requests
from bluesky_auth import BlueskyAuth

class FollowersFetcher:
    def __init__(self, auth: BlueskyAuth):
        self.auth = auth
        self.base_url = "https://bsky.social/xrpc"

    def get_all_followers(self, actor: Optional[str] = None) -> List[Dict]:
        """
        Fetch all followers for a given actor.
        Handles pagination automatically.
        """
        if not actor:
            actor = self.auth.login()["did"]

        followers = []
        cursor = None

        while True:
            params = {"actor": actor, "limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = requests.get(
                f"{self.base_url}/app.bsky.graph.getFollowers",
                headers=self.auth.get_auth_headers(),
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            followers.extend(data["followers"])
            
            cursor = data.get("cursor")
            if not cursor:
                break

        return followers

    def extract_follower_info(self, followers: List[Dict]) -> List[Dict]:
        """Extract relevant information from follower objects"""
        return [{
            'did': follower['did'],
            'handle': follower['handle'],
            'display_name': follower.get('displayName', '')
        } for follower in followers]


def main():
    auth = BlueskyAuth()
    fetcher = FollowersFetcher(auth)
    
    try:
        # Get all followers
        followers = fetcher.get_all_followers()
        
        # Extract and print follower information
        follower_info = fetcher.extract_follower_info(followers)
        
        print(f"Total followers: {len(follower_info)}")
        for follower in follower_info:
            print(f"Handle: {follower['handle']}")
            if follower['display_name']:
                print(f"Display Name: {follower['display_name']}")
            print(f"DID: {follower['did']}")
            print("---")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()