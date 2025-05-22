import os
import json
import webbrowser
import customtkinter as ctk
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from spotify_auth import SpotifyAuthManager
from playlist_manager import PlaylistManager
from analytics import MusicAnalytics

class MusicPlaylistApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("MoodySongs")
        self.geometry("1200x700")
        
        # Initialize variables
        self.spotify = None
        self.current_user = None
        self.current_theme = "dark"
        self.auth_manager = SpotifyAuthManager()
        
        # Create main layout
        self.create_layout()
        
        # Initialize managers
        self.auth_manager = SpotifyAuthManager()
        success, message = self.auth_manager.authenticate()
        
        if success:
            self.spotify = self.auth_manager.get_spotify_client()
            self.current_user = self.auth_manager.get_current_user()
            self.playlist_manager = PlaylistManager(self.spotify)
            self.analytics = MusicAnalytics(self.spotify)
        else:
            self.spotify = None
            self.current_user = None
            self.show_error(message)
    
    def create_layout(self):
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MoodySongs", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))
        
        # Navigation buttons
        self.nav_buttons = []
        for text, command in [
            ("Dashboard", self.show_dashboard),
            ("Search", self.show_search),
            ("Recommendations", self.show_recommendations),
            ("My Playlists", self.show_playlists),
            ("Analytics", self.show_analytics)
        ]:
            button = ctk.CTkButton(self.sidebar_frame, text=text, command=command)
            button.pack(padx=20, pady=10, fill="x")
            self.nav_buttons.append(button)
        
        # Theme switch
        self.theme_switch = ctk.CTkSwitch(self.sidebar_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(padx=20, pady=(20, 10))
        self.theme_switch.select()  # Default to dark mode
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Default to dashboard view
        self.show_dashboard()
    
    def initialize_spotify(self):
        """Initialize Spotify connection if not already done"""
        if not self.spotify:
            try:
                success, message = self.auth_manager.authenticate()
                
                if success:
                    self.spotify = self.auth_manager.get_spotify_client()
                    self.current_user = self.auth_manager.get_current_user()
                    self.playlist_manager = PlaylistManager(self.spotify)
                    self.analytics = MusicAnalytics(self.spotify)
                else:
                    self.show_error(message)
                
                # Update login status
                self.update_login_status()
            except Exception as e:
                self.show_error(f"Failed to connect to Spotify: {str(e)}")
        else:
            # Already initialized
            self.update_login_status()
    
    def update_login_status(self):
        if hasattr(self, 'login_label'):
            self.login_label.destroy()
        
        if self.current_user:
            text = f"Logged in as: {self.current_user['display_name']}"
        else:
            text = "Not logged in"
        
        self.login_label = ctk.CTkLabel(self.sidebar_frame, text=text)
        self.login_label.pack(padx=20, pady=(10, 20))
    
    def toggle_theme(self):
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
            self.theme_switch.deselect()
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.theme_switch.select()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        
        # Welcome message
        welcome = ctk.CTkLabel(
            self.content_frame, 
            text="Welcome to Interactive Music Playlist", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome.pack(padx=20, pady=20)
        
        # Quick stats
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(padx=20, pady=20, fill="x")
        
        # If logged in, show some user stats
        if self.spotify and self.current_user:
            try:
                # Get recently played tracks
                recent = self.spotify.current_user_recently_played(limit=5)
                
                # Display recent tracks
                recent_label = ctk.CTkLabel(
                    stats_frame, 
                    text="Recently Played Tracks", 
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                recent_label.pack(padx=10, pady=10)
                
                for i, item in enumerate(recent['items']):
                    track_name = item['track']['name']
                    artist_name = item['track']['artists'][0]['name']
                    track_label = ctk.CTkLabel(
                        stats_frame, 
                        text=f"{i+1}. {track_name} - {artist_name}"
                    )
                    track_label.pack(padx=10, pady=2, anchor="w")
            except Exception as e:
                error_label = ctk.CTkLabel(
                    stats_frame, 
                    text=f"Could not load recent tracks: {str(e)}"
                )
                error_label.pack(padx=10, pady=10)
        else:
            login_prompt = ctk.CTkLabel(
                stats_frame, 
                text="Please log in to Spotify to see your personalized dashboard"
            )
            login_prompt.pack(padx=10, pady=10)
            
            login_button = ctk.CTkButton(
                stats_frame, 
                text="Login to Spotify", 
                command=self.initialize_spotify
            )
            login_button.pack(padx=10, pady=10)
    
    def show_search(self):
        self.clear_content()
        
        # Search header
        header = ctk.CTkLabel(
            self.content_frame, 
            text="Search Music", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(padx=20, pady=20)
        
        # Search input
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(padx=20, pady=10, fill="x")
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search for songs, artists, or albums...")
        search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: self.perform_search(search_entry.get()))
        search_button.pack(side="right", padx=10, pady=10)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    def perform_search(self, query):
        if not query or not self.spotify:
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        try:
            # Search Spotify
            results = self.spotify.search(q=query, limit=10)
            
            # Display track results
            if results['tracks']['items']:
                tracks_label = ctk.CTkLabel(
                    self.results_frame, 
                    text="Tracks", 
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                tracks_label.pack(padx=10, pady=(10, 5), anchor="w")
                
                for i, track in enumerate(results['tracks']['items']):
                    track_frame = ctk.CTkFrame(self.results_frame)
                    track_frame.pack(padx=10, pady=5, fill="x")
                    
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    
                    track_label = ctk.CTkLabel(
                        track_frame, 
                        text=f"{track_name} - {artist_name}"
                    )
                    track_label.pack(side="left", padx=10, pady=10)
                    
                    preview_button = ctk.CTkButton(
                        track_frame, 
                        text="Preview", 
                        width=80,
                        command=lambda url=track['preview_url']: self.preview_track(url)
                    )
                    preview_button.pack(side="right", padx=10, pady=10)
            else:
                no_results = ctk.CTkLabel(
                    self.results_frame, 
                    text="No tracks found"
                )
                no_results.pack(padx=10, pady=10)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.results_frame, 
                text=f"Search error: {str(e)}"
            )
            error_label.pack(padx=10, pady=10)
    
    def preview_track(self, url):
        if url:
            webbrowser.open(url)
        else:
            self.show_error("No preview available for this track")
    
    def show_recommendations(self):
        self.clear_content()
        
        # Recommendations header
        header = ctk.CTkLabel(
            self.content_frame, 
            text="Mood-Based Recommendations", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(padx=20, pady=20)
        
        # Mood selection
        mood_frame = ctk.CTkFrame(self.content_frame)
        mood_frame.pack(padx=20, pady=10, fill="x")
        
        mood_label = ctk.CTkLabel(mood_frame, text="Select your mood:")
        mood_label.pack(padx=10, pady=10, anchor="w")
        
        moods = ["Happy", "Sad", "Energetic", "Chill", "Focused"]
        mood_buttons_frame = ctk.CTkFrame(mood_frame)
        mood_buttons_frame.pack(padx=10, pady=10, fill="x")
        
        for i, mood in enumerate(moods):
            mood_button = ctk.CTkButton(
                mood_buttons_frame, 
                text=mood, 
                command=lambda m=mood: self.get_mood_recommendations(m)
            )
            mood_button.grid(row=0, column=i, padx=5, pady=5)
        
        # Results frame
        self.recommendations_frame = ctk.CTkFrame(self.content_frame)
        self.recommendations_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    def get_mood_recommendations(self, mood):
        if not self.spotify:
            self.show_error("Please log in to Spotify first")
            return
        
        # Clear previous results
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()
        
        try:
            # Use playlist manager to get recommendations
            recommendations = self.playlist_manager.get_mood_recommendations(mood, limit=10)
            
            if not recommendations:
                self.show_error("No recommendations found for this mood")
                return
            
            # Display recommendations
            mood_label = ctk.CTkLabel(
                self.recommendations_frame, 
                text=f"{mood} Recommendations", 
                font=ctk.CTkFont(size=18, weight="bold")
            )
            mood_label.pack(padx=10, pady=(10, 5), anchor="w")
            
            # Create playlist button
            create_playlist_button = ctk.CTkButton(
                self.recommendations_frame,
                text=f"Create {mood} Playlist",
                command=lambda: self.create_playlist(mood, [track['id'] for track in recommendations])
            )
            create_playlist_button.pack(padx=10, pady=10)
            
            # Display tracks
            for i, track in enumerate(recommendations):
                track_frame = ctk.CTkFrame(self.recommendations_frame)
                track_frame.pack(padx=10, pady=5, fill="x")
                
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                
                track_label = ctk.CTkLabel(
                    track_frame, 
                    text=f"{i+1}. {track_name} - {artist_name}"
                )
                track_label.pack(side="left", padx=10, pady=10)
                
                preview_button = ctk.CTkButton(
                    track_frame, 
                    text="Preview", 
                    width=80,
                    command=lambda url=track['preview_url']: self.preview_track(url)
                )
                preview_button.pack(side="right", padx=10, pady=10)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.recommendations_frame, 
                text=f"Error getting recommendations: {str(e)}"
            )
            error_label.pack(padx=10, pady=10)
    
    def create_playlist(self, name, track_ids):
        if not self.spotify or not self.current_user:
            self.show_error("Please log in to Spotify first")
            return
        
        try:
            # Use playlist manager to create playlist
            success, result = self.playlist_manager.create_mood_playlist(name, track_ids)
            
            if success:
                # Show success message
                self.show_message(f"Created {name} playlist successfully!")
            else:
                self.show_error(result)
        except Exception as e:
            self.show_error(f"Failed to create playlist: {str(e)}")
    
    def show_playlists(self):
        self.clear_content()
        
        # Playlists header
        header = ctk.CTkLabel(
            self.content_frame, 
            text="My Playlists", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(padx=20, pady=20)
        
        if not self.spotify or not self.current_user:
            login_prompt = ctk.CTkLabel(
                self.content_frame, 
                text="Please log in to Spotify to see your playlists"
            )
            login_prompt.pack(padx=20, pady=20)
            return
        
        try:
            # Get user's playlists using playlist manager
            playlists = self.playlist_manager.get_user_playlists(limit=20)
            
            if not playlists:
                no_playlists = ctk.CTkLabel(
                    self.content_frame, 
                    text="You don't have any playlists yet"
                )
                no_playlists.pack(padx=20, pady=20)
                return
            
            # Display playlists
            playlists_frame = ctk.CTkScrollableFrame(self.content_frame)
            playlists_frame.pack(padx=20, pady=10, fill="both", expand=True)
            
            for i, playlist in enumerate(playlists):
                playlist_frame = ctk.CTkFrame(playlists_frame)
                playlist_frame.pack(padx=10, pady=5, fill="x")
                
                name = playlist['name']
                tracks = playlist['tracks']['total']
                
                playlist_label = ctk.CTkLabel(
                    playlist_frame, 
                    text=f"{name} ({tracks} tracks)"
                )
                playlist_label.pack(side="left", padx=10, pady=10)
                
                view_button = ctk.CTkButton(
                    playlist_frame, 
                    text="View", 
                    width=80,
                    command=lambda p_id=playlist['id']: self.view_playlist(p_id)
                )
                view_button.pack(side="right", padx=10, pady=10)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.content_frame, 
                text=f"Error loading playlists: {str(e)}"
            )
            error_label.pack(padx=20, pady=20)
    
    def view_playlist(self, playlist_id):
        if not self.spotify:
            self.show_error("Please log in to Spotify first")
            return
            
        try:
            # Get playlist details
            playlist = self.spotify.playlist(playlist_id)
            tracks = self.spotify.playlist_tracks(playlist_id, limit=50)
            
            # Create a new window for playlist details
            playlist_window = ctk.CTkToplevel(self)
            playlist_window.title(f"Playlist: {playlist['name']}")
            playlist_window.geometry("800x600")
            
            # Playlist header
            header_frame = ctk.CTkFrame(playlist_window)
            header_frame.pack(padx=20, pady=10, fill="x")
            
            name_label = ctk.CTkLabel(
                header_frame, 
                text=playlist['name'], 
                font=ctk.CTkFont(size=20, weight="bold")
            )
            name_label.pack(padx=10, pady=10, anchor="w")
            
            if 'description' in playlist and playlist['description']:
                desc_label = ctk.CTkLabel(
                    header_frame, 
                    text=playlist['description'],
                    wraplength=700
                )
                desc_label.pack(padx=10, pady=5, anchor="w")
            
            # Track list
            tracks_frame = ctk.CTkScrollableFrame(playlist_window)
            tracks_frame.pack(padx=20, pady=10, fill="both", expand=True)
            
            for i, item in enumerate(tracks['items']):
                track = item['track']
                if not track:  # Skip if track is None
                    continue
                    
                track_frame = ctk.CTkFrame(tracks_frame)
                track_frame.pack(padx=10, pady=5, fill="x")
                
                track_name = track['name']
                artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
                
                track_label = ctk.CTkLabel(
                    track_frame, 
                    text=f"{i+1}. {track_name} - {artist_name}"
                )
                track_label.pack(side="left", padx=10, pady=10)
                
                preview_button = ctk.CTkButton(
                    track_frame, 
                    text="Preview", 
                    width=80,
                    command=lambda url=track.get('preview_url'): self.preview_track(url)
                )
                preview_button.pack(side="right", padx=10, pady=10)
        except Exception as e:
            self.show_error(f"Error loading playlist: {str(e)}")
    
    def show_analytics(self):
        self.clear_content()
        
        # Analytics header
        header = ctk.CTkLabel(
            self.content_frame, 
            text="Listening Analytics", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(padx=20, pady=20)
        
        if not self.spotify or not self.current_user:
            login_prompt = ctk.CTkLabel(
                self.content_frame, 
                text="Please log in to Spotify to see your analytics"
            )
            login_prompt.pack(padx=20, pady=20)
            return
        
        try:
            # Create tabs for different analytics
            tabs_frame = ctk.CTkFrame(self.content_frame)
            tabs_frame.pack(padx=20, pady=10, fill="x")
            
            tab_buttons = []
            for text, command in [
                ("Top Genres", lambda: self.show_genre_chart()),
                ("Listening Time", lambda: self.show_listening_time()),
                ("Audio Features", lambda: self.show_audio_features())
            ]:
                button = ctk.CTkButton(tabs_frame, text=text, command=command)
                button.pack(side="left", padx=10, pady=10, expand=True)
                tab_buttons.append(button)
            
            # Chart frame
            self.chart_frame = ctk.CTkFrame(self.content_frame)
            self.chart_frame.pack(padx=20, pady=10, fill="both", expand=True)
            
            # Default to genre chart
            self.show_genre_chart()
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.content_frame, 
                text=f"Error loading analytics: {str(e)}"
            )
            error_label.pack(padx=20, pady=20)
    
    def show_genre_chart(self):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        try:
            # Use analytics module to create chart
            chart_widget = self.analytics.create_genre_chart(self.chart_frame)
            
            if chart_widget:
                chart_widget.pack(fill="both", expand=True)
            else:
                no_data = ctk.CTkLabel(
                    self.chart_frame, 
                    text="No listening data available"
                )
                no_data.pack(padx=20, pady=20)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame, 
                text=f"Error creating genre chart: {str(e)}"
            )
            error_label.pack(padx=20, pady=20)
    
    def show_listening_time(self):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        try:
            # Use analytics module to create chart
            chart_widget = self.analytics.create_listening_history_chart(self.chart_frame)
            
            if chart_widget:
                chart_widget.pack(fill="both", expand=True)
            else:
                no_data = ctk.CTkLabel(
                    self.chart_frame, 
                    text="No listening history available"
                )
                no_data.pack(padx=20, pady=20)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame, 
                text=f"Error creating listening chart: {str(e)}"
            )
            error_label.pack(padx=20, pady=20)
    
    def show_audio_features(self):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        try:
            # Use analytics module to create chart
            chart_widget = self.analytics.create_audio_features_chart(self.chart_frame)
            
            if chart_widget:
                chart_widget.pack(fill="both", expand=True)
            else:
                no_data = ctk.CTkLabel(
                    self.chart_frame, 
                    text="No audio features data available"
                )
                no_data.pack(padx=20, pady=20)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame, 
                text=f"Error creating audio features chart: {str(e)}"
            )
            error_label.pack(padx=20, pady=20)
    
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        
        error_label = ctk.CTkLabel(
            error_window, 
            text=message,
            wraplength=350
        )
        error_label.pack(padx=20, pady=20)
        
        ok_button = ctk.CTkButton(
            error_window, 
            text="OK", 
            command=error_window.destroy
        )
        ok_button.pack(padx=20, pady=20)
    
    def show_message(self, message):
        message_window = ctk.CTkToplevel(self)
        message_window.title("Message")
        message_window.geometry("400x200")
        
        message_label = ctk.CTkLabel(
            message_window, 
            text=message,
            wraplength=350
        )
        message_label.pack(padx=20, pady=20)
        
        ok_button = ctk.CTkButton(
            message_window, 
            text="OK", 
            command=message_window.destroy
        )
        ok_button.pack(padx=20, pady=20)

if __name__ == "__main__":
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run the application
    app = MusicPlaylistApp()
    app.mainloop()