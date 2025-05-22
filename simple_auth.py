import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

# Your Spotify API credentials
CLIENT_ID = "656c039e0dab41d39081647b76758480"
CLIENT_SECRET = "e77029c2d5314c9bb467af73914a9b6b"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-library-read user-top-read playlist-modify-public user-read-recently-played"

# Create the SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print(f"Please visit this URL to authorize the application: {auth_url}")
webbrowser.open(auth_url)

# Wait for the user to authorize and get the redirect URL
redirect_url = input("Enter the URL you were redirected to: ")

# Extract the code from the URL
code = sp_oauth.parse_response_code(redirect_url)

# Get the access token
token_info = sp_oauth.get_access_token(code)

# Create the Spotify client
sp = spotipy.Spotify(auth=token_info["access_token"])

# Test the connection
user = sp.current_user()
print(f"Successfully connected to Spotify as: {user['display_name']}")
print("You can now run the main application with: python main.py")

# Save the token to a file for the main app to use
with open(".spotify_token", "w") as f:
    f.write(token_info["access_token"])