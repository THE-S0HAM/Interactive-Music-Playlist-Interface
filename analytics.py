import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class MusicAnalytics:
    def __init__(self, spotify_client):
        self.spotify = spotify_client
        
    def get_top_genres_data(self):
        """Get user's top genres data for visualization"""
        try:
            # Get user's top artists
            top_artists = self.spotify.current_user_top_artists(limit=50, time_range="medium_term")
            
            if not top_artists['items']:
                return None
            
            # Extract genres
            all_genres = []
            for artist in top_artists['items']:
                all_genres.extend(artist['genres'])
            
            # Count genre occurrences
            genre_counts = {}
            for genre in all_genres:
                if genre in genre_counts:
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1
            
            # Get top genres
            top_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:8])
            return top_genres
        except Exception as e:
            print(f"Error getting top genres: {e}")
            return None
    
    def create_genre_chart(self, frame):
        """Create and display a pie chart of top genres"""
        top_genres = self.get_top_genres_data()
        
        if not top_genres:
            return None
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(top_genres.values(), labels=top_genres.keys(), autopct='%1.1f%%')
        ax.set_title('Your Top Genres')
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        return canvas.get_tk_widget()
    
    def get_audio_features_data(self):
        """Get audio features of user's top tracks"""
        try:
            # Get user's top tracks
            top_tracks = self.spotify.current_user_top_tracks(limit=20, time_range="medium_term")
            
            if not top_tracks['items']:
                return None
            
            # Get track IDs
            track_ids = [track['id'] for track in top_tracks['items']]
            
            # Get audio features for tracks
            audio_features = self.spotify.audio_features(track_ids)
            
            # Create dataframe
            tracks_data = []
            for i, features in enumerate(audio_features):
                if features:
                    track = top_tracks['items'][i]
                    tracks_data.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'danceability': features['danceability'],
                        'energy': features['energy'],
                        'valence': features['valence'],
                        'tempo': features['tempo'],
                        'acousticness': features['acousticness'],
                        'instrumentalness': features['instrumentalness']
                    })
            
            return pd.DataFrame(tracks_data)
        except Exception as e:
            print(f"Error getting audio features: {e}")
            return None
    
    def create_audio_features_chart(self, frame):
        """Create and display a radar chart of audio features"""
        df = self.get_audio_features_data()
        
        if df is None or df.empty:
            return None
        
        # Calculate average audio features
        avg_features = df[['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']].mean()
        
        # Create radar chart
        categories = list(avg_features.index)
        values = list(avg_features.values)
        
        # Add the first value at the end to close the circle
        values.append(values[0])
        categories.append(categories[0])
        
        # Calculate angle for each category
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles.append(angles[0])
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, values, linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
        ax.set_title('Your Music Profile')
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        return canvas.get_tk_widget()
    
    def get_listening_history_data(self):
        """Get user's recent listening history data"""
        try:
            # Get recently played tracks
            recent = self.spotify.current_user_recently_played(limit=50)
            
            if not recent['items']:
                return None
            
            # Create dataframe
            history_data = []
            for item in recent['items']:
                track = item['track']
                played_at = item['played_at']
                history_data.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'played_at': pd.to_datetime(played_at)
                })
            
            df = pd.DataFrame(history_data)
            df['date'] = df['played_at'].dt.date
            
            # Count plays per day
            plays_per_day = df.groupby('date').size().reset_index(name='count')
            plays_per_day['date'] = pd.to_datetime(plays_per_day['date'])
            plays_per_day = plays_per_day.sort_values('date')
            
            return plays_per_day
        except Exception as e:
            print(f"Error getting listening history: {e}")
            return None
    
    def create_listening_history_chart(self, frame):
        """Create and display a bar chart of listening history"""
        df = self.get_listening_history_data()
        
        if df is None or df.empty:
            return None
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(df['date'], df['count'])
        ax.set_xlabel('Date')
        ax.set_ylabel('Tracks Played')
        ax.set_title('Your Listening Activity')
        
        # Format x-axis dates
        fig.autofmt_xdate()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        return canvas.get_tk_widget()