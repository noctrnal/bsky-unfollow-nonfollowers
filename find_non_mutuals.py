import json

class BlueskyMutuals:
    def __init__(self):
        self.followers = set()
        self.follows = set()
        
    def load_data(self, followers_file="followers.json", follows_file="follows.json"):
        """
        Load followers and follows data from JSON files
        """
        # Load followers
        with open(followers_file, 'r', encoding='utf-8') as f:
            followers_data = json.load(f)
            self.followers = {user["did"] for user in followers_data}
            
        # Load follows
        with open(follows_file, 'r', encoding='utf-8') as f:
            follows_data = json.load(f)
            self.follows = {user["did"] for user in follows_data}
            
        # Store full user data for later reference
        self.followers_data = {user["did"]: user for user in followers_data}
        self.follows_data = {user["did"]: user for user in follows_data}
    
    def find_non_mutuals(self):
        """
        Find users who are not mutual followers
        
        Returns:
            dict: Contains two lists - 'non_mutual_followers' and 'non_mutual_follows'
        """
        # People who follow you but you don't follow back
        non_mutual_followers = self.followers - self.follows
        
        # People you follow but don't follow you back
        non_mutual_follows = self.follows - self.followers
        
        # Convert DIDs back to full user data
        non_mutual_followers_data = [
            self.followers_data[did] for did in non_mutual_followers
        ]
        
        non_mutual_follows_data = [
            self.follows_data[did] for did in non_mutual_follows
        ]
        
        return {
            "non_mutual_followers": non_mutual_followers_data,
            "non_mutual_follows": non_mutual_follows_data
        }
    
    def save_non_mutuals(self):
        """
        Save non-mutual relationships to separate JSON files
        """
        non_mutuals = self.find_non_mutuals()
        
        # Save non-mutual followers
        with open('non_mutual_followers.json', 'w', encoding='utf-8') as f:
            json.dump(non_mutuals['non_mutual_followers'], f, indent=2)
            
        # Save non-mutual follows
        with open('non_mutual_follows.json', 'w', encoding='utf-8') as f:
            json.dump(non_mutuals['non_mutual_follows'], f, indent=2)
            
        print(f"Found {len(non_mutuals['non_mutual_followers'])} users who follow you but you don't follow back")
        print(f"Saved to non_mutual_followers.json")
        print(f"\nFound {len(non_mutuals['non_mutual_follows'])} users you follow but don't follow you back")
        print(f"Saved to non_mutual_follows.json")

def main():
    bm = BlueskyMutuals()
    bm.load_data()
    bm.save_non_mutuals()

if __name__ == "__main__":
    main() 