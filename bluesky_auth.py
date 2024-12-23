import requests
from typing import Dict, Optional
import os
from dotenv import load_dotenv

class BlueskyAuth:
    BASE_URL = "https://bsky.social/xrpc"
    
    def __init__(self):
        load_dotenv()
        self.session_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def login(self, identifier: str = None, password: str = None) -> Dict:
        """
        Authenticate with Bluesky and get session tokens.
        """
        identifier = identifier or os.getenv('BLUESKY_IDENTIFIER')
        password = password or os.getenv('BLUESKY_PASSWORD')
        
        if not identifier or not password:
            raise ValueError("Bluesky credentials not provided and not found in environment")
            
        response = requests.post(
            f"{self.BASE_URL}/com.atproto.server.createSession",
            json={"identifier": identifier, "password": password}
        )
        response.raise_for_status()
        
        auth_data = response.json()
        self.session_token = auth_data.get('accessJwt')
        self.refresh_token = auth_data.get('refreshJwt')
        
        return auth_data
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get headers needed for authenticated requests."""
        if not self.session_token:
            raise ValueError("Not authenticated. Call login() first")
            
        return {
            "Authorization": f"Bearer {self.session_token}",
            "Content-Type": "application/json"
        } 