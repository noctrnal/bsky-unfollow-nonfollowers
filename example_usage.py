from bluesky_auth import BlueskyAuth
from analyze_relationships import RelationshipAnalyzer
from unfollow_manager import UnfollowManager

# Initialize auth and managers
auth = BlueskyAuth()
analyzer = RelationshipAnalyzer(auth)
unfollow_manager = UnfollowManager(auth)

# First, analyze relationships
analysis = analyzer.get_relationship_analysis()
print(f"\nFound {len(analysis['non_mutual_follows'])} non-mutual follows")

# Do a dry run first to see what would happen
print("\nPerforming dry run...")
results = unfollow_manager.unfollow_non_mutuals(dry_run=True)

# Ask for confirmation
response = input("\nWould you like to proceed with unfollowing? (yes/no): ")
if response.lower() == "yes":
    # Proceed with actual unfollowing
    results = unfollow_manager.unfollow_non_mutuals(dry_run=False)
    
    print("\n=== Results ===")
    print(f"Successfully unfollowed: {results['successful']}")
    print(f"Failed to unfollow: {results['failed']}")
    
    if results["failures"]:
        print("\nFailed to unfollow these users:")
        for handle in results["failures"]:
            print(f"@{handle}")
else:
    print("Operation cancelled") 