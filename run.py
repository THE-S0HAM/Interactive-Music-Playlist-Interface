import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def setup_spotify():
    """Set up Spotify authentication and return client"""
    # Check if config file exists
    if not os.path.exists("config.json"):
        print("Error: config.json file not found.")
        print("Please create a config.json file with your Spotify API credentials.")
        sys.exit(1)
    
    # Load credentials
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            client_id = config.get("client_id")
            client_secret = config.get("client_secret")
    except Exception as e:
        print(f"Error loading credentials: {e}")
        sys.exit(1)
    
    # Check if credentials are valid
    if not client_id or not client_secret:
        print("Error: Missing Spotify API credentials in config.json")
        sys.exit(1)
    
    # Remove cache file if it exists
    if os.path.exists(".spotify_cache"):
        try:
            os.remove(".spotify_cache")
            print("Removed old authentication cache.")
        except:
            pass
    
    # Set up authentication
    redirect_uri = "http://localhost:8888/callback"
    scope = "user-library-read user-top-read playlist-modify-public user-read-recently-played"
    
    try:
        print("Authenticating with Spotify...")
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=True,
            show_dialog=True
        )
        
        # Get token (this will open browser for authentication)
        token = auth_manager.get_access_token(as_dict=False)
        
        # Create Spotify client
        spotify = spotipy.Spotify(auth=token)
        
        # Test connection
        user = spotify.current_user()
        print(f"Successfully authenticated as: {user['display_name']}")
        
        return True
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

if __name__ == "__main__":
    # Set up Spotify
    if setup_spotify():
        # If authentication successful, run the main app
        print("Starting MoodySongs application...")
        import main
    else:
        print("Failed to authenticate with Spotify. Please check your credentials and try again.")