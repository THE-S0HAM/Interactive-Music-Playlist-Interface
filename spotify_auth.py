import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAuthManager:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = "http://localhost:8888/callback"
        self.scope = "user-library-read user-top-read playlist-modify-public user-read-recently-played"
        self.spotify = None
        self.user = None
        
        # Try to load credentials from config file
        self.load_credentials()
    
    def load_credentials(self):
        """Load Spotify API credentials from config file"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)
                    self.client_id = config.get("client_id")
                    self.client_secret = config.get("client_secret")
        except Exception as e:
            print(f"Error loading credentials: {e}")
    
    def save_credentials(self, client_id, client_secret):
        """Save Spotify API credentials to config file"""
        try:
            config = {
                "client_id": client_id,
                "client_secret": client_secret
            }
            with open("config.json", "w") as f:
                json.dump(config, f)
            self.client_id = client_id
            self.client_secret = client_secret
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
    
    def authenticate(self):
        """Authenticate with Spotify API"""
        if not self.client_id or not self.client_secret:
            return False, "Missing Spotify API credentials"
        
        try:
            # Simple direct authentication
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope
            )
            
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
            self.user = self.spotify.current_user()
            return True, "Authentication successful"
        except Exception as e:
            print(f"Authentication error: {e}")
            return False, f"Authentication failed: {str(e)}"
    
    def get_spotify_client(self):
        """Get authenticated Spotify client"""
        return self.spotify
    
    def get_current_user(self):
        """Get current user information"""
        return self.user