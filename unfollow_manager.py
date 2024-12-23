from typing import Dict, Optional
import requests
from bluesky_auth import BlueskyAuth
from analyze_relationships import RelationshipAnalyzer

class UnfollowManager:
    def __init__(self, auth: BlueskyAuth):
        self.auth = auth
        self.base_url = "https://bsky.social/xrpc"
        self.analyzer = RelationshipAnalyzer(auth)

    def get_follow_record(self, target_did: str) -> Optional[Dict]:
        """Get the follow record for a specific user"""
        my_did = self.auth.login()["did"]
        cursor = None

        while True:
            params = {"actor": my_did, "limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = requests.get(
                f"{self.base_url}/app.bsky.graph.getFollows",
                headers=self.auth.get_auth_headers(),
                params=params
            )
            response.raise_for_status()
            data = response.json()

            for follow in data["follows"]:
                if follow["did"] == target_did:
                    return {
                        "uri": follow["uri"],
                        "rkey": follow["uri"].split("/")[-1],
                        "did": follow["did"],
                        "handle": follow["handle"]
                    }

            cursor = data.get("cursor")
            if not cursor:
                break

        return None

    def unfollow_user(self, target_did: str) -> bool:
        """Unfollow a specific user"""
        try:
            follow_record = self.get_follow_record(target_did)
            if not follow_record:
                print(f"No follow record found for DID: {target_did}")
                return False

            my_did = self.auth.login()["did"]
            
            response = requests.post(
                f"{self.base_url}/com.atproto.repo.deleteRecord",
                headers=self.auth.get_auth_headers(),
                json={
                    "collection": "app.bsky.graph.follow",
                    "repo": my_did,
                    "rkey": follow_record["rkey"]
                }
            )
            response.raise_for_status()
            
            print(f"Successfully unfollowed @{follow_record['handle']}")
            return True

        except Exception as e:
            print(f"Failed to unfollow user: {str(e)}")
            return False

    def unfollow_non_mutuals(self, dry_run: bool = True) -> Dict:
        """Unfollow all non-mutual follows"""
        analysis = self.analyzer.get_relationship_analysis()
        non_mutuals = analysis["non_mutual_follows"]
        
        results = {
            "total_attempted": len(non_mutuals),
            "successful": 0,
            "failed": 0,
            "failures": []
        }
        
        print(f"\nFound {len(non_mutuals)} non-mutual follows")
        
        if dry_run:
            print("\nDRY RUN - No users will be unfollowed")
            print("\nWould unfollow these users:")
            for user in non_mutuals:
                print(f"@{user['handle']} ({user['did']})")
            return results
        
        print("\nProceeding with unfollow operation...")
        for user in non_mutuals:
            if self.unfollow_user(user["did"]):
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["failures"].append(user["handle"])
        
        return results 