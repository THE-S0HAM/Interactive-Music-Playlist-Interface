"""
Revamped Music Playlist Interface with modern UI
"""
import os
import json
import webbrowser
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import spotipy
from spotify_auth import SpotifyAuthManager
from playlist_manager import PlaylistManager
from analytics import MusicAnalytics
from player import MusicPlayer

class RevampedMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("MoodySongs - Premium")
        self.geometry("1280x720")
        self.minsize(1000, 600)
        
        # Initialize variables
        self.spotify = None
        self.current_user = None
        self.current_theme = "dark"
        self.auth_manager = SpotifyAuthManager()
        self.music_player = MusicPlayer()
        
        # Create main layout
        self.create_layout()
        
        # Initialize Spotify connection
        self.initialize_spotify()
        
        # Cleanup on window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_layout(self):
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Header in content area
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        # Main content container (changes based on navigation)
        self.main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Default to dashboard view
        self.show_dashboard()
    
    def create_sidebar(self):
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)  # Push settings to bottom
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="MoodySongs",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Search", self.show_search),
            ("Recommendations", self.show_recommendations),
            ("My Playlists", self.show_playlists),
            ("Analytics", self.show_analytics)
        ]
        
        for i, (text, command) in enumerate(nav_items):
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                command=command,
                anchor="w",
                height=40,
                corner_radius=8
            )
            button.grid(row=i+1, column=0, padx=20, pady=10, sticky="ew")
            self.nav_buttons.append(button)
        
        # Theme switch at bottom
        self.appearance_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance:")
        self.appearance_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame, 
            text="Dark Mode",
            command=self.toggle_theme
        )
        self.theme_switch.grid(row=9, column=0, padx=20, pady=(5, 10), sticky="w")
        self.theme_switch.select()  # Default to dark mode
        
        # User info at bottom
        self.user_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.user_frame.grid(row=10, column=0, padx=20, pady=20, sticky="ew")
        
        self.user_label = ctk.CTkLabel(self.user_frame, text="Not logged in")
        self.user_label.pack(anchor="w")
    
    def initialize_spotify(self):
        """Initialize Spotify connection"""
        try:
            success, message = self.auth_manager.authenticate()
            
            if success:
                self.spotify = self.auth_manager.get_spotify_client()
                self.current_user = self.auth_manager.get_current_user()
                self.playlist_manager = PlaylistManager(self.spotify)
                self.analytics = MusicAnalytics(self.spotify)
                self.update_user_info()
            else:
                self.show_error(message)
        except Exception as e:
            self.show_error(f"Failed to connect to Spotify: {str(e)}")
    
    def update_user_info(self):
        """Update user info in sidebar"""
        if self.current_user:
            self.user_label.configure(text=f"Logged in as: {self.current_user['display_name']}")
        else:
            self.user_label.configure(text="Not logged in")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
            self.theme_switch.deselect()
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.theme_switch.select()
    
    def clear_main_container(self):
        """Clear the main container for new content"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def update_header(self, title):
        """Update the header with a new title"""
        for widget in self.header_frame.winfo_children():
            widget.destroy()
            
        header_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(anchor="w")
        
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_main_container()
        self.update_header("Dashboard")
        
        # Create dashboard layout
        dashboard = ctk.CTkFrame(self.main_container, fg_color="transparent")
        dashboard.pack(fill="both", expand=True)
        
        # Welcome message
        if self.current_user:
            welcome_text = f"Welcome back, {self.current_user['display_name']}!"
        else:
            welcome_text = "Welcome to MoodySongs!"
            
        welcome = ctk.CTkLabel(
            dashboard, 
            text=welcome_text,
            font=ctk.CTkFont(size=20)
        )
        welcome.pack(pady=(0, 20), anchor="w")
        
        # Quick stats in cards
        stats_frame = ctk.CTkFrame(dashboard)
        stats_frame.pack(fill="x", pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="stats")
        
        # Stats cards
        self.create_stat_card(stats_frame, "Recently Played", "5 tracks", 0, 0)
        self.create_stat_card(stats_frame, "Top Genre", "Pop", 0, 1)
        self.create_stat_card(stats_frame, "Mood Today", "Energetic", 0, 2)
        
        # Recently played section
        recent_frame = ctk.CTkFrame(dashboard)
        recent_frame.pack(fill="both", expand=True, pady=20)
        
        recent_label = ctk.CTkLabel(
            recent_frame, 
            text="Recently Played",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        recent_label.pack(padx=15, pady=(15, 10), anchor="w")
        
        # If logged in, show recent tracks
        if self.spotify and self.current_user:
            try:
                recent = self.spotify.current_user_recently_played(limit=5)
                
                if recent['items']:
                    for i, item in enumerate(recent['items']):
                        track = item['track']
                        track_frame = ctk.CTkFrame(recent_frame)
                        track_frame.pack(fill="x", padx=15, pady=5)
                        
                        track_name = track['name']
                        artist_name = track['artists'][0]['name']
                        
                        # Track number
                        num_label = ctk.CTkLabel(track_frame, text=f"{i+1}", width=30)
                        num_label.pack(side="left", padx=(10, 0), pady=10)
                        
                        # Track info
                        info_frame = ctk.CTkFrame(track_frame, fg_color="transparent")
                        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
                        
                        name_label = ctk.CTkLabel(
                            info_frame, 
                            text=track_name,
                            font=ctk.CTkFont(weight="bold")
                        )
                        name_label.pack(anchor="w")
                        
                        artist_label = ctk.CTkLabel(info_frame, text=artist_name)
                        artist_label.pack(anchor="w")
                        
                        # Album art
                        album_art = None
                        if 'album' in track and 'images' in track['album'] and track['album']['images']:
                            album_image_url = track['album']['images'][-1]['url']  # Get smallest image
                            album_art = self.load_album_art(album_image_url, (40, 40))
                        
                        # Album art display
                        if album_art:
                            art_label = ctk.CTkLabel(track_frame, image=album_art, text="")
                            art_label.pack(side="left", padx=(10, 0), pady=10)
                            
                        # Preview button
                        preview_button = ctk.CTkButton(
                            track_frame, 
                            text="Play", 
                            width=80,
                            command=lambda url=track['preview_url'], tid=track['id']: self.preview_track(url, tid)
                        )
                        preview_button.pack(side="right", padx=10, pady=10)
                else:
                    no_tracks = ctk.CTkLabel(recent_frame, text="No recently played tracks")
                    no_tracks.pack(padx=15, pady=15)
            except Exception as e:
                error_label = ctk.CTkLabel(recent_frame, text=f"Could not load recent tracks: {str(e)}")
                error_label.pack(padx=15, pady=15)
        else:
            # Login prompt
            login_frame = ctk.CTkFrame(recent_frame, fg_color="transparent")
            login_frame.pack(padx=15, pady=15, fill="both", expand=True)
            
            login_label = ctk.CTkLabel(
                login_frame, 
                text="Please log in to Spotify to see your personalized dashboard"
            )
            login_label.pack(pady=(0, 10))
            
            login_button = ctk.CTkButton(
                login_frame, 
                text="Login to Spotify", 
                command=self.initialize_spotify
            )
            login_button.pack()
    
    def create_stat_card(self, parent, title, value, row, column):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
        
        title_label = ctk.CTkLabel(
            card, 
            text=title,
            font=ctk.CTkFont(size=14)
        )
        title_label.pack(padx=15, pady=(15, 5), anchor="w")
        
        value_label = ctk.CTkLabel(
            card, 
            text=value,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        value_label.pack(padx=15, pady=(0, 15), anchor="w")
        
    def show_search(self):
        """Show search view"""
        self.clear_main_container()
        self.update_header("Search Music")
        
        # Create search layout
        search_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        search_container.pack(fill="both", expand=True)
        
        # Search bar
        search_frame = ctk.CTkFrame(search_container, height=50, corner_radius=25)
        search_frame.pack(fill="x", pady=(0, 20))
        search_frame.pack_propagate(False)
        
        search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search for songs, artists, or albums...",
            border_width=0,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=5)
        
        search_button = ctk.CTkButton(
            search_frame, 
            text="Search",
            width=100,
            height=35,
            command=lambda: self.perform_search(search_entry.get())
        )
        search_button.pack(side="right", padx=(10, 10), pady=7)
        
        # Results frame
        self.results_frame = ctk.CTkScrollableFrame(search_container)
        self.results_frame.pack(fill="both", expand=True)
    
    def perform_search(self, query):
        """Perform search and display results"""
        if not query or not self.spotify:
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        try:
            # Search Spotify
            results = self.spotify.search(q=query, limit=15, type="track,artist,album")
            
            # Display track results
            if results['tracks']['items']:
                # Section header
                tracks_header = ctk.CTkFrame(self.results_frame, fg_color="transparent", height=40)
                tracks_header.pack(fill="x", pady=(5, 10))
                
                tracks_label = ctk.CTkLabel(
                    tracks_header, 
                    text="Tracks",
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                tracks_label.pack(side="left")
                
                # Track results
                for track in results['tracks']['items']:
                    self.create_track_item(track)
            else:
                no_tracks = ctk.CTkLabel(self.results_frame, text="No tracks found")
                no_tracks.pack(pady=10)
                
            # Display artist results if available
            if 'artists' in results and results['artists']['items']:
                artists_header = ctk.CTkFrame(self.results_frame, fg_color="transparent", height=40)
                artists_header.pack(fill="x", pady=(20, 10))
                
                artists_label = ctk.CTkLabel(
                    artists_header, 
                    text="Artists",
                    font=ctk.CTkFont(size=18, weight="bold")
                )
                artists_label.pack(side="left")
                
                # Artist grid
                artists_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
                artists_frame.pack(fill="x", pady=10)
                artists_frame.grid_columnconfigure((0, 1, 2), weight=1)
                
                # Display artists in grid
                for i, artist in enumerate(results['artists']['items'][:6]):
                    row = i // 3
                    col = i % 3
                    self.create_artist_card(artists_frame, artist, row, col)
                    
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.results_frame, 
                text=f"Search error: {str(e)}"
            )
            error_label.pack(pady=20)
    
    def create_track_item(self, track):
        """Create a track item in search results"""
        track_frame = ctk.CTkFrame(self.results_frame, height=70)
        track_frame.pack(fill="x", pady=5)
        track_frame.pack_propagate(False)
        
        # Track info
        track_name = track['name']
        artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
        
        # Album art
        album_art = None
        if 'album' in track and 'images' in track['album'] and track['album']['images']:
            album_image_url = track['album']['images'][-1]['url']  # Get smallest image
            album_art = self.load_album_art(album_image_url, (50, 50))
        
        # Album art display
        if album_art:
            art_label = ctk.CTkLabel(track_frame, image=album_art, text="")
            art_label.pack(side="left", padx=(10, 0), pady=10)
        
        # Track info container
        info_frame = ctk.CTkFrame(track_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame, 
            text=track_name,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(anchor="w")
        
        artist_label = ctk.CTkLabel(
            info_frame, 
            text=artist_name,
            font=ctk.CTkFont(size=12)
        )
        artist_label.pack(anchor="w")
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(track_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10)
        
        preview_button = ctk.CTkButton(
            buttons_frame, 
            text="Play", 
            width=80,
            height=30,
            command=lambda url=track.get('preview_url'), tid=track.get('id'): self.preview_track(url, tid)
        )
        preview_button.pack(side="right", padx=5)
    
    def create_artist_card(self, parent, artist, row, col):
        """Create an artist card in grid layout"""
        card = ctk.CTkFrame(parent, width=150, height=100, corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        name_label = ctk.CTkLabel(
            card, 
            text=artist['name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=130
        )
        name_label.pack(expand=True)
        
    def preview_track(self, url=None, track_id=None):
        """Play track preview using the music player or open in Spotify"""
        from player import MusicPlayer
        
        # Create player if not exists
        if not hasattr(self, 'music_player'):
            self.music_player = MusicPlayer()
        
        # Play the track
        success, message = self.music_player.play(url, track_id)
        
        if not success:
            # If track_id is None but we have a URL, try to extract ID from URL
            if track_id is None and url and 'spotify.com/track/' in url:
                try:
                    track_id = url.split('spotify.com/track/')[1].split('?')[0]
                    success, message = self.music_player.play(None, track_id)
                except:
                    pass
            
            # If still not successful, show error
            if not success:
                # Always open in Spotify if possible
                if track_id:
                    webbrowser.open(f"https://open.spotify.com/track/{track_id}")
                    self.show_message("Opening track in Spotify", "Information")
                else:
                    self.show_error("No playable source available")
            
    def show_recommendations(self):
        """Show recommendations view"""
        self.clear_main_container()
        self.update_header("Mood-Based Recommendations")
        
        # Create recommendations layout
        recommendations_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        recommendations_container.pack(fill="both", expand=True)
        
        # Mood selection section
        mood_section = ctk.CTkFrame(recommendations_container)
        mood_section.pack(fill="x", pady=(0, 20))
        
        mood_label = ctk.CTkLabel(
            mood_section, 
            text="How are you feeling today?",
            font=ctk.CTkFont(size=16)
        )
        mood_label.pack(padx=20, pady=(20, 15))
        
        # Mood buttons
        moods_frame = ctk.CTkFrame(mood_section, fg_color="transparent")
        moods_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        moods = ["Happy", "Sad", "Energetic", "Chill", "Focused"]
        mood_colors = ["#FFD700", "#6495ED", "#FF4500", "#9370DB", "#3CB371"]
        
        for i, (mood, color) in enumerate(zip(moods, mood_colors)):
            mood_button = ctk.CTkButton(
                moods_frame, 
                text=mood,
                fg_color=color,
                hover_color=color,
                text_color="#000000" if mood == "Happy" else "#FFFFFF",
                width=100,
                height=40,
                corner_radius=20,
                command=lambda m=mood: self.get_mood_recommendations(m)
            )
            mood_button.pack(side="left", padx=(0 if i == 0 else 10), expand=True)
        
        # Results section
        self.recommendations_frame = ctk.CTkScrollableFrame(recommendations_container)
        self.recommendations_frame.pack(fill="both", expand=True)
        
        # Initial prompt
        prompt_label = ctk.CTkLabel(
            self.recommendations_frame, 
            text="Select a mood to get personalized recommendations",
            font=ctk.CTkFont(size=14)
        )
        prompt_label.pack(pady=50)
    
    def get_mood_recommendations(self, mood):
        """Get and display mood-based recommendations"""
        if not self.spotify:
            self.show_error("Please log in to Spotify first")
            return
        
        # Clear previous results
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()
        
        # Show loading indicator
        loading_label = ctk.CTkLabel(
            self.recommendations_frame, 
            text=f"Finding {mood} tracks for you...",
            font=ctk.CTkFont(size=14)
        )
        loading_label.pack(pady=20)
        self.update_idletasks()
        
        try:
            # Get recommendations
            recommendations = self.playlist_manager.get_mood_recommendations(mood, limit=10)
            
            # Remove loading indicator
            loading_label.destroy()
            
            if not recommendations:
                no_results = ctk.CTkLabel(
                    self.recommendations_frame, 
                    text="No recommendations found for this mood"
                )
                no_results.pack(pady=20)
                return
            
            # Header with mood
            mood_header = ctk.CTkFrame(self.recommendations_frame, fg_color="transparent")
            mood_header.pack(fill="x", pady=(0, 10))
            
            mood_label = ctk.CTkLabel(
                mood_header, 
                text=f"{mood} Recommendations",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            mood_label.pack(side="left")
            
            # Create playlist button
            create_playlist_button = ctk.CTkButton(
                mood_header,
                text=f"Create {mood} Playlist",
                command=lambda: self.create_playlist(mood, [track['id'] for track in recommendations])
            )
            create_playlist_button.pack(side="right")
            
            # Display recommendations
            for i, track in enumerate(recommendations):
                track_frame = ctk.CTkFrame(self.recommendations_frame, height=70)
                track_frame.pack(fill="x", pady=5)
                track_frame.pack_propagate(False)
                
                # Track number
                num_label = ctk.CTkLabel(track_frame, text=f"{i+1}", width=30)
                num_label.pack(side="left", padx=(15, 0))
                
                # Track info
                track_name = track['name']
                artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
                
                # Album art
                album_art = None
                if 'album' in track and 'images' in track['album'] and track['album']['images']:
                    album_image_url = track['album']['images'][-1]['url']  # Get smallest image
                    album_art = self.load_album_art(album_image_url, (50, 50))
                
                # Album art display
                if album_art:
                    art_label = ctk.CTkLabel(track_frame, image=album_art, text="")
                    art_label.pack(side="left", padx=(10, 0), pady=10)
                
                info_frame = ctk.CTkFrame(track_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
                
                name_label = ctk.CTkLabel(
                    info_frame, 
                    text=track_name,
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                name_label.pack(anchor="w")
                
                artist_label = ctk.CTkLabel(
                    info_frame, 
                    text=artist_name,
                    font=ctk.CTkFont(size=12)
                )
                artist_label.pack(anchor="w")
                
                # Preview button
                preview_button = ctk.CTkButton(
                    track_frame, 
                    text="Play", 
                    width=80,
                    height=30,
                    command=lambda url=track.get('preview_url'), tid=track.get('id'): self.preview_track(url, tid)
                )
                preview_button.pack(side="right", padx=15, pady=15)
                
        except Exception as e:
            # Remove loading indicator
            loading_label.destroy()
            
            error_label = ctk.CTkLabel(
                self.recommendations_frame, 
                text=f"Error getting recommendations: {str(e)}"
            )
            error_label.pack(pady=20)
    
    def create_playlist(self, name, track_ids):
        """Create a new playlist with selected tracks"""
        if not self.spotify or not self.current_user:
            self.show_error("Please log in to Spotify first")
            return
        
        try:
            # Use playlist manager to create playlist
            success, result = self.playlist_manager.create_mood_playlist(name, track_ids)
            
            if success:
                self.show_message(f"Created {name} playlist successfully!")
            else:
                self.show_error(result)
        except Exception as e:
            self.show_error(f"Failed to create playlist: {str(e)}")
            
    def show_playlists(self):
        """Show user's playlists"""
        self.clear_main_container()
        self.update_header("My Playlists")
        
        # Create playlists layout
        playlists_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        playlists_container.pack(fill="both", expand=True)
        
        if not self.spotify or not self.current_user:
            # Login prompt
            login_frame = ctk.CTkFrame(playlists_container, fg_color="transparent")
            login_frame.pack(pady=50, fill="both", expand=True)
            
            login_label = ctk.CTkLabel(
                login_frame, 
                text="Please log in to Spotify to see your playlists",
                font=ctk.CTkFont(size=14)
            )
            login_label.pack(pady=(0, 15))
            
            login_button = ctk.CTkButton(
                login_frame, 
                text="Login to Spotify", 
                command=self.initialize_spotify
            )
            login_button.pack()
            return
        
        try:
            # Get user's playlists
            playlists = self.playlist_manager.get_user_playlists(limit=20)
            
            if not playlists:
                no_playlists = ctk.CTkLabel(
                    playlists_container, 
                    text="You don't have any playlists yet",
                    font=ctk.CTkFont(size=14)
                )
                no_playlists.pack(pady=50)
                return
            
            # Create grid layout for playlists
            playlists_frame = ctk.CTkScrollableFrame(playlists_container)
            playlists_frame.pack(fill="both", expand=True)
            
            # Display playlists in a grid
            for i, playlist in enumerate(playlists):
                self.create_playlist_card(playlists_frame, playlist, i)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                playlists_container, 
                text=f"Error loading playlists: {str(e)}"
            )
            error_label.pack(pady=50)
    
    def create_playlist_card(self, parent, playlist, index):
        """Create a playlist card"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)
        
        # Playlist info
        name = playlist['name']
        tracks_count = playlist['tracks']['total']
        
        # Layout
        card.grid_columnconfigure(1, weight=1)
        
        # Playlist icon/number
        icon_label = ctk.CTkLabel(
            card, 
            text=f"{index+1}",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=40,
            height=40
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=(15, 10), pady=15)
        
        # Playlist name
        name_label = ctk.CTkLabel(
            card, 
            text=name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.grid(row=0, column=1, padx=5, pady=(15, 0), sticky="w")
        
        # Tracks count
        tracks_label = ctk.CTkLabel(
            card, 
            text=f"{tracks_count} tracks"
        )
        tracks_label.grid(row=1, column=1, padx=5, pady=(0, 15), sticky="w")
        
        # View button
        view_button = ctk.CTkButton(
            card, 
            text="View", 
            width=80,
            command=lambda p_id=playlist['id']: self.view_playlist(p_id)
        )
        view_button.grid(row=0, column=2, rowspan=2, padx=15, pady=15)
    
    def view_playlist(self, playlist_id):
        """Show playlist details in a new window"""
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
            playlist_window.minsize(600, 400)
            
            # Configure grid
            playlist_window.grid_columnconfigure(0, weight=1)
            playlist_window.grid_rowconfigure(2, weight=1)
            
            # Playlist header
            header_frame = ctk.CTkFrame(playlist_window)
            header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
            
            name_label = ctk.CTkLabel(
                header_frame, 
                text=playlist['name'], 
                font=ctk.CTkFont(size=24, weight="bold")
            )
            name_label.pack(padx=15, pady=15, anchor="w")
            
            # Description if available
            if 'description' in playlist and playlist['description']:
                desc_frame = ctk.CTkFrame(playlist_window)
                desc_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 0))
                
                desc_label = ctk.CTkLabel(
                    desc_frame, 
                    text=playlist['description'],
                    wraplength=760
                )
                desc_label.pack(padx=15, pady=15, anchor="w")
            
            # Track list
            tracks_frame = ctk.CTkScrollableFrame(playlist_window)
            tracks_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
            
            # Column headers
            headers_frame = ctk.CTkFrame(tracks_frame, fg_color="transparent")
            headers_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            # Header labels
            ctk.CTkLabel(headers_frame, text="#", width=40).pack(side="left")
            ctk.CTkLabel(headers_frame, text="Title", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(10, 0), expand=True, fill="x")
            ctk.CTkLabel(headers_frame, text="Actions", width=80).pack(side="right", padx=10)
            
            # Separator
            separator = ctk.CTkFrame(tracks_frame, height=1)
            separator.pack(fill="x", padx=10, pady=(0, 10))
            
            # Display tracks
            for i, item in enumerate(tracks['items']):
                track = item['track']
                if not track:  # Skip if track is None
                    continue
                    
                track_frame = ctk.CTkFrame(tracks_frame, fg_color="transparent")
                track_frame.pack(fill="x", padx=10, pady=2)
                
                # Track number
                num_label = ctk.CTkLabel(track_frame, text=f"{i+1}", width=40)
                num_label.pack(side="left")
                
                # Track info
                track_name = track['name']
                artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
                
                info_frame = ctk.CTkFrame(track_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
                
                name_label = ctk.CTkLabel(
                    info_frame, 
                    text=track_name,
                    font=ctk.CTkFont(weight="bold"),
                    anchor="w"
                )
                name_label.pack(fill="x")
                
                artist_label = ctk.CTkLabel(
                    info_frame, 
                    text=artist_name,
                    anchor="w"
                )
                artist_label.pack(fill="x")
                
                # Album art
                album_art = None
                if 'album' in track and 'images' in track['album'] and track['album']['images']:
                    album_image_url = track['album']['images'][-1]['url']  # Get smallest image
                    album_art = self.load_album_art(album_image_url, (40, 40))
                
                # Album art display
                if album_art:
                    art_label = ctk.CTkLabel(track_frame, image=album_art, text="")
                    art_label.pack(side="left", padx=(5, 0))
                
                # Preview button
                preview_button = ctk.CTkButton(
                    track_frame, 
                    text="Play", 
                    width=80,
                    command=lambda url=track.get('preview_url'), tid=track.get('id'): self.preview_track(url, tid)
                )
                preview_button.pack(side="right", padx=10)
        except Exception as e:
            self.show_error(f"Error loading playlist: {str(e)}")
            
    def show_analytics(self):
        """Show analytics view"""
        self.clear_main_container()
        self.update_header("Listening Analytics")
        
        # Create analytics layout
        analytics_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        analytics_container.pack(fill="both", expand=True)
        
        if not self.spotify or not self.current_user:
            # Login prompt
            login_frame = ctk.CTkFrame(analytics_container, fg_color="transparent")
            login_frame.pack(pady=50, fill="both", expand=True)
            
            login_label = ctk.CTkLabel(
                login_frame, 
                text="Please log in to Spotify to see your analytics",
                font=ctk.CTkFont(size=14)
            )
            login_label.pack(pady=(0, 15))
            
            login_button = ctk.CTkButton(
                login_frame, 
                text="Login to Spotify", 
                command=self.initialize_spotify
            )
            login_button.pack()
            return
        
        try:
            # Create tabs for different analytics
            tabs_frame = ctk.CTkFrame(analytics_container)
            tabs_frame.pack(fill="x", pady=(0, 20))
            
            # Tab buttons
            tab_buttons = []
            tabs = [
                ("Top Genres", lambda: self.show_genre_chart()),
                ("Listening Time", lambda: self.show_listening_time()),
                ("Audio Features", lambda: self.show_audio_features())
            ]
            
            for i, (text, command) in enumerate(tabs):
                button = ctk.CTkButton(
                    tabs_frame, 
                    text=text, 
                    command=command,
                    fg_color="transparent" if i > 0 else None,
                    border_width=0,
                    corner_radius=0
                )
                button.pack(side="left", padx=0, pady=0, fill="x", expand=True)
                tab_buttons.append(button)
            
            # Chart frame
            self.chart_frame = ctk.CTkFrame(analytics_container)
            self.chart_frame.pack(fill="both", expand=True)
            
            # Default to genre chart
            self.show_genre_chart()
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                analytics_container, 
                text=f"Error loading analytics: {str(e)}"
            )
            error_label.pack(pady=50)
    
    def show_genre_chart(self):
        """Show genre chart in analytics"""
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
                    text="No genre data available",
                    font=ctk.CTkFont(size=14)
                )
                no_data.pack(pady=50)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame, 
                text=f"Error creating genre chart: {str(e)}"
            )
            error_label.pack(pady=50)
    
    def show_listening_time(self):
        """Show listening time chart in analytics"""
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
                    text="No listening history available",
                    font=ctk.CTkFont(size=14)
                )
                no_data.pack(pady=50)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame, 
                text=f"Error creating listening chart: {str(e)}"
            )
            error_label.pack(pady=50)
    
    def show_audio_features(self):
        """Show audio features chart in analytics"""
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
                    text="No audio features data available",
                    font=ctk.CTkFont(size=14)
                )
                no_data.pack(pady=50)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_frame, 
                text=f"Error creating audio features chart: {str(e)}"
            )
            error_label.pack(pady=50)
    
    def show_error(self, message):
        """Show error message in a popup"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        
        # Center the window
        error_window.update_idletasks()
        width = error_window.winfo_width()
        height = error_window.winfo_height()
        x = (error_window.winfo_screenwidth() // 2) - (width // 2)
        y = (error_window.winfo_screenheight() // 2) - (height // 2)
        error_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Error icon/symbol
        error_frame = ctk.CTkFrame(error_window, fg_color="#FF5252", width=50, height=50, corner_radius=25)
        error_frame.pack(pady=(20, 10))
        error_frame.pack_propagate(False)
        
        error_symbol = ctk.CTkLabel(
            error_frame, 
            text="!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        error_symbol.place(relx=0.5, rely=0.5, anchor="center")
        
        # Error message
        error_label = ctk.CTkLabel(
            error_window, 
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=14)
        )
        error_label.pack(padx=20, pady=10)
        
        # OK button
        ok_button = ctk.CTkButton(
            error_window, 
            text="OK", 
            command=error_window.destroy,
            width=100
        )
        ok_button.pack(pady=20)
    
    def load_album_art(self, url, size=(100, 100)):
        """Load album art from URL and return as CTkImage"""
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                img = img.resize(size, Image.LANCZOS)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            return None
        except Exception as e:
            print(f"Error loading album art: {e}")
            return None
    
    def on_closing(self):
        """Handle window closing event"""
        # Clean up music player resources
        if hasattr(self, 'music_player'):
            self.music_player.cleanup()
        self.destroy()
    
    def show_message(self, message, title="Success"):
        """Show message in a popup with custom title"""
        message_window = ctk.CTkToplevel(self)
        message_window.title(title)
        message_window.geometry("400x200")
        message_window.resizable(False, False)
        
        # Center the window
        message_window.update_idletasks()
        width = message_window.winfo_width()
        height = message_window.winfo_height()
        x = (message_window.winfo_screenwidth() // 2) - (width // 2)
        y = (message_window.winfo_screenheight() // 2) - (height // 2)
        message_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Icon color based on title
        icon_color = "#4EE6A2"  # Default green for success
        icon_text = "✓"
        
        if title.lower() == "error":
            icon_color = "#FF5252"  # Red for error
            icon_text = "!"
        elif title.lower() == "information":
            icon_color = "#00C9FF"  # Blue for info
            icon_text = "i"
        
        # Message icon/symbol
        icon_frame = ctk.CTkFrame(message_window, fg_color=icon_color, width=50, height=50, corner_radius=25)
        icon_frame.pack(pady=(20, 10))
        icon_frame.pack_propagate(False)
        
        icon_symbol = ctk.CTkLabel(
            icon_frame, 
            text=icon_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        icon_symbol.place(relx=0.5, rely=0.5, anchor="center")
        
        # Message text
        message_label = ctk.CTkLabel(
            message_window, 
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=14)
        )
        message_label.pack(padx=20, pady=10)
        
        # OK button
        ok_button = ctk.CTkButton(
            message_window, 
            text="OK", 
            command=message_window.destroy,
            width=100
        )
        ok_button.pack(pady=20)