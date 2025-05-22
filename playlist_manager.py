import json
import os

class PlaylistManager:
    def __init__(self, spotify_client):
        self.spotify = spotify_client
        self.user_id = None
        if self.spotify:
            user = self.spotify.current_user()
            self.user_id = user['id'] if user else None
    
    def create_mood_playlist(self, mood, track_ids):
        """Create a new playlist based on mood"""
        if not self.spotify or not self.user_id or not track_ids:
            return False, "Missing required data"
        
        try:
            # Create a new playlist
            playlist = self.spotify.user_playlist_create(
                user=self.user_id,
                name=f"{mood} Playlist",
                public=True,
                description=f"Generated {mood} playlist from MoodySongs App"
            )
            
            # Add tracks to playlist
            self.spotify.playlist_add_items(playlist['id'], track_ids)
            
            return True, playlist['id']
        except Exception as e:
            return False, f"Failed to create playlist: {str(e)}"
    
    def get_user_playlists(self, limit=50):
        """Get user's playlists"""
        if not self.spotify or not self.user_id:
            return []
        
        try:
            playlists = self.spotify.current_user_playlists(limit=limit)
            return playlists['items']
        except Exception as e:
            print(f"Error getting playlists: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id, limit=100):
        """Get tracks from a playlist"""
        if not self.spotify:
            return []
        
        try:
            results = self.spotify.playlist_tracks(playlist_id, limit=limit)
            return results['items']
        except Exception as e:
            print(f"Error getting playlist tracks: {e}")
            return []
    
    def get_mood_recommendations(self, mood, limit=20):
        """Get track recommendations based on mood"""
        if not self.spotify:
            return []
        
        try:
            # Map moods to audio features
            mood_params = {
                "Happy": {"target_valence": 0.8, "target_energy": 0.7},
                "Sad": {"target_valence": 0.2, "target_energy": 0.3},
                "Energetic": {"target_valence": 0.6, "target_energy": 0.9},
                "Chill": {"target_valence": 0.5, "target_energy": 0.3},
                "Focused": {"target_valence": 0.5, "target_energy": 0.5, "target_instrumentalness": 0.5}
            }
            
            # Get user's top tracks for seed
            top_tracks = self.spotify.current_user_top_tracks(limit=5, time_range="medium_term")
            if not top_tracks['items']:
                return []
                
            seed_tracks = [track['id'] for track in top_tracks['items'][:2]]
            
            # Get recommendations
            params = mood_params.get(mood, {})
            recommendations = self.spotify.recommendations(
                seed_tracks=seed_tracks, 
                limit=limit,
                **params
            )
            
            return recommendations['tracks']
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def save_session(self, data, filename="session.json"):
        """Save session data to file"""
        try:
            with open(filename, "w") as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def load_session(self, filename="session.json"):
        """Load session data from file"""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading session: {e}")
            return {}