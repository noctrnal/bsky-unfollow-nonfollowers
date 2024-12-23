from typing import List, Dict
from bluesky_auth import BlueskyAuth
from get_followers import FollowersFetcher
from get_follows import FollowsFetcher

class RelationshipAnalyzer:
    def __init__(self, auth: BlueskyAuth):
        self.auth = auth
        self.followers_fetcher = FollowersFetcher(auth)
        self.follows_fetcher = FollowsFetcher(auth)

    def get_relationship_analysis(self, actor: str = None) -> Dict:
        """
        Analyze the relationships between followers and follows.
        """
        # Fetch all followers and follows
        followers = self.followers_fetcher.get_all_followers(actor)
        follows = self.follows_fetcher.get_all_follows(actor)

        # Convert to sets of DIDs for efficient comparison
        follower_dids = {f['did'] for f in followers}
        following_dids = {f['did'] for f in follows}

        # Create lookup dictionaries
        follower_lookup = {f['did']: f for f in followers}
        following_lookup = {f['did']: f for f in follows}

        # Find relationship categories
        mutual_dids = follower_dids & following_dids
        non_mutual_dids = following_dids - follower_dids
        fans_dids = follower_dids - following_dids

        # Convert DIDs back to user information
        mutual_follows = [following_lookup[did] for did in mutual_dids]
        non_mutual_follows = [following_lookup[did] for did in non_mutual_dids]
        fans = [follower_lookup[did] for did in fans_dids]

        return {
            "mutual_follows": self.followers_fetcher.extract_follower_info(mutual_follows),
            "non_mutual_follows": self.follows_fetcher.extract_follow_info(non_mutual_follows),
            "fans": self.followers_fetcher.extract_follower_info(fans),
            "counts": {
                "total_followers": len(followers),
                "total_following": len(follows),
                "mutual_follows": len(mutual_follows),
                "non_mutual_follows": len(non_mutual_follows),
                "fans": len(fans)
            }
        }

    def print_analysis(self, analysis: Dict):
        """Print a formatted analysis report"""
        counts = analysis["counts"]
        print("\n=== Relationship Analysis ===")
        print(f"\nTotal Followers: {counts['total_followers']}")
        print(f"Total Following: {counts['total_following']}")
        print(f"Mutual Follows: {counts['mutual_follows']}")
        print(f"Non-Mutual Follows: {counts['non_mutual_follows']}")
        print(f"Fans: {counts['fans']}")

        print("\n=== Non-Mutual Follows (Users who don't follow you back) ===")
        for user in analysis["non_mutual_follows"]:
            print(f"\nHandle: {user['handle']}")
            if user['display_name']:
                print(f"Display Name: {user['display_name']}")
            print(f"DID: {user['did']}")

def main():
    auth = BlueskyAuth()
    analyzer = RelationshipAnalyzer(auth)
    
    try:
        analysis = analyzer.get_relationship_analysis()
        analyzer.print_analysis(analysis)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 