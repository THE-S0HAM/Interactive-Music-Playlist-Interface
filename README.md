# Interactive Music Playlist Interface

A modern, feature-rich music playlist application that integrates with Spotify to provide personalized music recommendations, analytics, and playlist management.

## Features

- **Modern UI**: Clean, responsive interface with dark and light mode support
- **Spotify Integration**: Connect to your Spotify account to access your music library
- **Mood-Based Recommendations**: Get music recommendations based on your current mood
- **Playlist Management**: Create, view, and manage your Spotify playlists
- **Music Analytics**: Visualize your listening habits with interactive charts
- **Search**: Find songs, artists, and albums with an intuitive search interface

## Screenshots

(Screenshots will be added after running the application)

## Requirements

- Python 3.7+
- Spotify Developer Account (for API access)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/Interactive-Music-Playlist-Interface.git
cd Interactive-Music-Playlist-Interface
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Create a Spotify Developer Application at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Set the redirect URI to `http://127.0.0.1:8888/callback`
   - Note your Client ID and Client Secret

4. Create a `config.json` file in the project root with your Spotify credentials:
```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret"
}
```

## Usage

1. Run the application:
```
python revamped_main.py
```

2. Log in with your Spotify account when prompted
3. Explore music, create playlists, and enjoy your personalized music experience!

## Original vs Revamped Interface

This project includes both the original interface (`main.py`) and a completely revamped interface with improved design and user experience (`revamped_main.py`).

To run the original interface:
```
python main.py
```

To run the revamped interface:
```
python revamped_main.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.