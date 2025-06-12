import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAuthManager:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = "http://127.0.0.1:8888/callback"  # Must match exactly what's in Spotify Dashboard
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
            # Check if we have tokens from the simple auth process
            if os.path.exists(".spotify_tokens"):
                with open(".spotify_tokens", "r") as f:
                    tokens = json.load(f)
                    access_token = tokens.get("access_token")
                    if access_token:
                        self.spotify = spotipy.Spotify(auth=access_token)
                        self.user = self.spotify.current_user()
                        return True, "Authentication successful using saved token"
            
            # If no tokens or token failed, use standard OAuth
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri="http://127.0.0.1:8888/callback",  # Use exact URI from Spotify Dashboard
                scope=self.scope,
                open_browser=False  # Don't open browser automatically
            )
            
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
            self.user = self.spotify.current_user()
            return True, "Authentication successful"
        except Exception as e:
            print(f"Authentication error: {e}")
            print("Please run spotify_simple_auth.py first to authenticate")
            return False, f"Authentication failed: {str(e)}"
    
    def get_spotify_client(self):
        """Get authenticated Spotify client"""
        return self.spotify
    
    def get_current_user(self):
        """Get current user information"""
        return self.user