import os
from dotenv import load_dotenv
import requests
from typing import Dict, Optional

class BlueskyAuth:
    def __init__(self):
        load_dotenv()
        self.api_url = "https://bsky.social/xrpc"
        self.session: Optional[Dict] = None
        
    def login(self) -> Dict:
        """
        Authenticate with Bluesky using credentials from environment variables
        Returns the session data including access token
        """
        identifier = os.getenv("BLUESKY_IDENTIFIER")
        password = os.getenv("BLUESKY_PASSWORD")
        
        if not identifier or not password:
            raise ValueError("Missing Bluesky credentials in environment variables")
            
        auth_response = requests.post(
            f"{self.api_url}/com.atproto.server.createSession",
            json={"identifier": identifier, "password": password}
        )
        
        if auth_response.status_code != 200:
            raise Exception(f"Authentication failed: {auth_response.text}")
            
        self.session = auth_response.json()
        return self.session
    
    def get_auth_header(self) -> Dict[str, str]:
        """
        Returns the authorization header needed for authenticated requests
        """
        if not self.session:
            self.login()
        
        return {
            "Authorization": f"Bearer {self.session['accessJwt']}"
        }