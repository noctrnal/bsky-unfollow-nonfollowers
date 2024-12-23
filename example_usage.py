from bluesky_auth import BlueskyAuth

def main():
    # Initialize the auth handler
    auth = BlueskyAuth()
    
    # Get authentication headers
    headers = auth.get_auth_header()
    print("Successfully authenticated with Bluesky")
    
    # Now you can use these headers in your requests
    # Example:
    # response = requests.get(
    #     "https://bsky.social/xrpc/some-endpoint",
    #     headers=headers
    # )

if __name__ == "__main__":
    main()