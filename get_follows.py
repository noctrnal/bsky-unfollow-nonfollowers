from typing import List, Dict, Optional
import requests
from bluesky_auth import BlueskyAuth

class FollowsFetcher:
    def __init__(self, auth: BlueskyAuth):
        self.auth = auth
        self.base_url = "https://bsky.social/xrpc"

    def get_all_follows(self, actor: Optional[str] = None) -> List[Dict]:
        """
        Fetch all accounts that a given actor follows.
        Handles pagination automatically.
        """
        if not actor:
            actor = self.auth.login()["did"]

        follows = []
        cursor = None

        while True:
            params = {"actor": actor, "limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = requests.get(
                f"{self.base_url}/app.bsky.graph.getFollows",
                headers=self.auth.get_auth_headers(),
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            follows.extend(data["follows"])
            
            cursor = data.get("cursor")
            if not cursor:
                break

        return follows

    def extract_follow_info(self, follows: List[Dict]) -> List[Dict]:
        """Extract relevant information from follow objects"""
        return [{
            'did': follow['did'],
            'handle': follow['handle'],
            'display_name': follow.get('displayName', ''),
            'description': follow.get('description', '')
        } for follow in follows]


def main():
    # Example usage
    auth = BlueskyAuth()
    fetcher = FollowsFetcher(auth)
    
    try:
        # Get all accounts the user follows
        follows = fetcher.get_all_follows()
        
        # Extract and print follow information
        follow_info = fetcher.extract_follow_info(follows)
        
        print(f"Total accounts following: {len(follow_info)}")
        for follow in follow_info:
            print(f"Handle: {follow['handle']}")
            if follow['display_name']:
                print(f"Display Name: {follow['display_name']}")
            print(f"DID: {follow['did']}")
            if follow['description']:
                print(f"Bio: {follow['description']}")
            print("---")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 