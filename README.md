# MoodySongs

A desktop application that integrates with Spotify to provide an interactive music playlist experience based on your mood.

## Features

- Connect to your Spotify account
- Search for songs, artists, and albums
- Get mood-based music recommendations
- Create and manage playlists
- View listening analytics and statistics
- Dark/light mode toggle

## Requirements

- Python 3.8+
- Spotify Developer Account (for API credentials)

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/Interactive-Music-Playlist-Interface.git
cd Interactive-Music-Playlist-Interface
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a Spotify Developer Application:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application
   - Set the redirect URI to `http://localhost:8888/callback`
   - Note your Client ID and Client Secret

4. Create a `config.json` file in the project root with your Spotify credentials:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

## Usage

Run the application:
```
python main.py
```

## Project Structure

- `main.py`: Application entry point
- `app.py`: Main application class and UI
- `spotify_auth.py`: Spotify authentication manager
- `playlist_manager.py`: Playlist creation and management
- `analytics.py`: Music listening analytics and visualization

## Author
### Soham Deshmukh  

## License

MIT