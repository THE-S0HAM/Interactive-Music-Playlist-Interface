import customtkinter as ctk
import random
import pygame
import os
import time
from threading import Thread

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.paused = False
        self.playing = False
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        
    def play(self, track_path):
        if self.playing and self.current_track == track_path:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.paused = True
        else:
            try:
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
                self.current_track = track_path
                self.playing = True
                self.paused = False
            except Exception as e:
                print(f"Error playing track: {e}")
                
    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        
    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
        
    def seek(self, seconds):
        current_pos = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
        new_pos = current_pos + seconds
        if new_pos < 0:
            new_pos = 0
        pygame.mixer.music.play(start=new_pos)
        
    def forward(self):
        self.seek(10)
        
    def backward(self):
        self.seek(-10)
        
    def is_playing(self):
        return self.playing and not self.paused

class DemoMusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("MoodySongs Demo")
        self.geometry("1200x700")
        
        # Initialize variables
        self.current_theme = "dark"
        self.music_player = MusicPlayer()
        self.current_track_info = {"name": "", "artist": ""}
        
        # Sample tracks (local files)
        self.sample_tracks_dir = "sample_tracks"
        self.available_tracks = self.get_available_tracks()
        self.current_track_index = 0
        
        # Create main layout
        self.create_layout()
    
    def get_available_tracks(self):
        """Get list of available MP3 files in the sample_tracks directory"""
        tracks = []
        if os.path.exists(self.sample_tracks_dir):
            for file in os.listdir(self.sample_tracks_dir):
                if file.lower().endswith('.mp3'):
                    # Extract track name and artist from filename
                    name = os.path.splitext(file)[0]
                    # Try to split by dash if present
                    if " - " in name:
                        parts = name.split(" - ", 1)
                        artist = parts[0].strip()
                        title = parts[1].strip()
                    else:
                        artist = "Unknown Artist"
                        title = name
                    
                    tracks.append({
                        "file": os.path.join(self.sample_tracks_dir, file),
                        "name": title,
                        "artist": artist
                    })
        
        # If no tracks found, add placeholder
        if not tracks:
            tracks = [
                {"file": None, "name": "Demo Track 1", "artist": "Demo Artist"},
                {"file": None, "name": "Demo Track 2", "artist": "Demo Artist"},
                {"file": None, "name": "Demo Track 3", "artist": "Demo Artist"}
            ]
        
        return tracks
    
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
        
        # Login status
        self.login_label = ctk.CTkLabel(self.sidebar_frame, text="Demo Mode - No Login Required")
        self.login_label.pack(padx=20, pady=(10, 20))
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Player controls at bottom
        self.create_player_controls()
        
        # Default to dashboard view
        self.show_dashboard()
    
    def create_player_controls(self):
        # Player frame at the bottom
        self.player_frame = ctk.CTkFrame(self)
        self.player_frame.pack(side="bottom", fill="x", padx=20, pady=10)
        
        # Track info
        self.track_info_frame = ctk.CTkFrame(self.player_frame)
        self.track_info_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.track_name_label = ctk.CTkLabel(self.track_info_frame, text="No track playing", font=ctk.CTkFont(size=14, weight="bold"))
        self.track_name_label.pack(anchor="w")
        
        self.track_artist_label = ctk.CTkLabel(self.track_info_frame, text="")
        self.track_artist_label.pack(anchor="w")
        
        # Controls frame
        controls_frame = ctk.CTkFrame(self.player_frame)
        controls_frame.pack(side="right", padx=10, pady=10)
        
        # Control buttons
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=5)
        
        self.backward_10_button = ctk.CTkButton(buttons_frame, text="◀◀ 10s", width=60, command=self.backward_10)
        self.backward_10_button.pack(side="left", padx=5)
        
        self.backward_button = ctk.CTkButton(buttons_frame, text="◀◀", width=40, command=self.previous_track)
        self.backward_button.pack(side="left", padx=5)
        
        self.play_button = ctk.CTkButton(buttons_frame, text="▶", width=60, command=self.toggle_play)
        self.play_button.pack(side="left", padx=5)
        
        self.forward_button = ctk.CTkButton(buttons_frame, text="▶▶", width=40, command=self.next_track)
        self.forward_button.pack(side="left", padx=5)
        
        self.forward_10_button = ctk.CTkButton(buttons_frame, text="10s ▶▶", width=60, command=self.forward_10)
        self.forward_10_button.pack(side="left", padx=5)
        
        # Volume control
        volume_frame = ctk.CTkFrame(controls_frame)
        volume_frame.pack(pady=5)
        
        volume_label = ctk.CTkLabel(volume_frame, text="Volume:")
        volume_label.pack(side="left", padx=5)
        
        self.volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=1, number_of_steps=10, command=self.set_volume)
        self.volume_slider.pack(side="left", padx=5, fill="x", expand=True)
        self.volume_slider.set(0.5)  # Default volume
    
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
            text="Welcome to MoodySongs Demo", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome.pack(padx=20, pady=20)
        
        # Demo info
        info = ctk.CTkLabel(
            self.content_frame,
            text="This is a demo version with basic playback functionality.\nClick on any track to play audio.",
            font=ctk.CTkFont(size=16)
        )
        info.pack(padx=20, pady=10)
        
        # Quick stats
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(padx=20, pady=20, fill="x")
        
        # Display sample tracks
        recent_label = ctk.CTkLabel(
            stats_frame, 
            text="Available Tracks", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        recent_label.pack(padx=10, pady=10)
        
        for i, track in enumerate(self.available_tracks):
            track_frame = ctk.CTkFrame(stats_frame)
            track_frame.pack(padx=10, pady=5, fill="x")
            
            track_label = ctk.CTkLabel(
                track_frame, 
                text=f"{i+1}. {track['name']} - {track['artist']}"
            )
            track_label.pack(side="left", padx=10, pady=10)
            
            play_button = ctk.CTkButton(
                track_frame, 
                text="Play", 
                width=60,
                command=lambda t=track, idx=i: self.play_track(t, idx)
            )
            play_button.pack(side="right", padx=10, pady=10)
    
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
        
        search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: self.show_demo_results())
        search_button.pack(side="right", padx=10, pady=10)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.content_frame)
        self.results_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Demo message
        demo_label = ctk.CTkLabel(
            self.results_frame,
            text="Enter a search term and click Search to see demo results",
            font=ctk.CTkFont(size=14)
        )
        demo_label.pack(padx=20, pady=20)
    
    def show_demo_results(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Display track results
        tracks_label = ctk.CTkLabel(
            self.results_frame, 
            text="Demo Results", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        tracks_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # Use available tracks for search results
        for i, track in enumerate(self.available_tracks):
            track_frame = ctk.CTkFrame(self.results_frame)
            track_frame.pack(padx=10, pady=5, fill="x")
            
            track_label = ctk.CTkLabel(
                track_frame, 
                text=f"{track['name']} - {track['artist']}"
            )
            track_label.pack(side="left", padx=10, pady=10)
            
            play_button = ctk.CTkButton(
                track_frame, 
                text="Play", 
                width=60,
                command=lambda t=track, idx=i: self.play_track(t, idx)
            )
            play_button.pack(side="right", padx=10, pady=10)
    
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
                command=lambda m=mood: self.show_demo_mood(m)
            )
            mood_button.grid(row=0, column=i, padx=5, pady=5)
        
        # Results frame
        self.recommendations_frame = ctk.CTkFrame(self.content_frame)
        self.recommendations_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Demo message
        demo_label = ctk.CTkLabel(
            self.recommendations_frame,
            text="Select a mood to see demo recommendations",
            font=ctk.CTkFont(size=14)
        )
        demo_label.pack(padx=20, pady=20)
    
    def show_demo_mood(self, mood):
        # Clear previous results
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()
        
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
            command=self.show_demo_message
        )
        create_playlist_button.pack(padx=10, pady=10)
        
        # Use available tracks for recommendations
        random.shuffle(self.available_tracks)
        
        # Display tracks
        for i, track in enumerate(self.available_tracks):
            track_frame = ctk.CTkFrame(self.recommendations_frame)
            track_frame.pack(padx=10, pady=5, fill="x")
            
            track_label = ctk.CTkLabel(
                track_frame, 
                text=f"{i+1}. {track['name']} - {track['artist']}"
            )
            track_label.pack(side="left", padx=10, pady=10)
            
            play_button = ctk.CTkButton(
                track_frame, 
                text="Play", 
                width=60,
                command=lambda t=track, idx=i: self.play_track(t, idx)
            )
            play_button.pack(side="right", padx=10, pady=10)
    
    def show_playlists(self):
        self.clear_content()
        
        # Playlists header
        header = ctk.CTkLabel(
            self.content_frame, 
            text="My Playlists", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(padx=20, pady=20)
        
        # Display playlists
        playlists_frame = ctk.CTkScrollableFrame(self.content_frame)
        playlists_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        sample_playlists = [
            {"name": "My Favorites", "tracks": len(self.available_tracks)},
            {"name": "Workout Mix", "tracks": len(self.available_tracks)},
            {"name": "Chill Vibes", "tracks": len(self.available_tracks)},
            {"name": "Road Trip", "tracks": len(self.available_tracks)},
            {"name": "Study Session", "tracks": len(self.available_tracks)}
        ]
        
        for playlist in sample_playlists:
            playlist_frame = ctk.CTkFrame(playlists_frame)
            playlist_frame.pack(padx=10, pady=5, fill="x")
            
            playlist_label = ctk.CTkLabel(
                playlist_frame, 
                text=f"{playlist['name']} ({playlist['tracks']} tracks)"
            )
            playlist_label.pack(side="left", padx=10, pady=10)
            
            view_button = ctk.CTkButton(
                playlist_frame, 
                text="View", 
                width=80,
                command=lambda p=playlist: self.view_demo_playlist(p)
            )
            view_button.pack(side="right", padx=10, pady=10)
    
    def view_demo_playlist(self, playlist):
        # Create a new window for playlist details
        playlist_window = ctk.CTkToplevel(self)
        playlist_window.title(f"Playlist: {playlist['name']}")
        playlist_window.geometry("600x500")
        
        # Playlist header
        header_frame = ctk.CTkFrame(playlist_window)
        header_frame.pack(padx=20, pady=10, fill="x")
        
        name_label = ctk.CTkLabel(
            header_frame, 
            text=playlist['name'], 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        name_label.pack(padx=10, pady=10, anchor="w")
        
        # Track list
        tracks_frame = ctk.CTkScrollableFrame(playlist_window)
        tracks_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Use available tracks for this playlist
        for i, track in enumerate(self.available_tracks):
            track_frame = ctk.CTkFrame(tracks_frame)
            track_frame.pack(padx=10, pady=5, fill="x")
            
            track_label = ctk.CTkLabel(
                track_frame, 
                text=f"{i+1}. {track['name']} - {track['artist']}"
            )
            track_label.pack(side="left", padx=10, pady=10)
            
            play_button = ctk.CTkButton(
                track_frame, 
                text="Play", 
                width=60,
                command=lambda t=track, idx=i: self.play_track(t, idx)
            )
            play_button.pack(side="right", padx=10, pady=10)
    
    def show_analytics(self):
        self.clear_content()
        
        # Analytics header
        header = ctk.CTkLabel(
            self.content_frame, 
            text="Listening Analytics", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(padx=20, pady=20)
        
        # Create tabs for different analytics
        tabs_frame = ctk.CTkFrame(self.content_frame)
        tabs_frame.pack(padx=20, pady=10, fill="x")
        
        tab_buttons = []
        for text in ["Top Genres", "Listening Time", "Audio Features"]:
            button = ctk.CTkButton(tabs_frame, text=text, command=self.show_demo_message)
            button.pack(side="left", padx=10, pady=10, expand=True)
            tab_buttons.append(button)
        
        # Demo analytics content
        analytics_frame = ctk.CTkFrame(self.content_frame)
        analytics_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        demo_label = ctk.CTkLabel(
            analytics_frame,
            text="Demo Analytics\n\nThis would display charts and statistics about your music listening habits.",
            font=ctk.CTkFont(size=14)
        )
        demo_label.pack(padx=20, pady=20)
    
    def show_demo_message(self):
        message_window = ctk.CTkToplevel(self)
        message_window.title("Demo Feature")
        message_window.geometry("400x200")
        
        message_label = ctk.CTkLabel(
            message_window, 
            text="This is a demo feature.\nIn the full version, this would connect to Spotify.",
            wraplength=350
        )
        message_label.pack(padx=20, pady=20)
        
        ok_button = ctk.CTkButton(
            message_window, 
            text="OK", 
            command=message_window.destroy
        )
        ok_button.pack(padx=20, pady=20)
    
    # Music player functions
    def play_track(self, track, index=None):
        if index is not None:
            self.current_track_index = index
            
        # Update track info
        self.current_track_info = track
        self.track_name_label.configure(text=track["name"])
        self.track_artist_label.configure(text=track["artist"])
        
        # Play the track if file exists
        if track["file"] and os.path.exists(track["file"]):
            self.music_player.play(track["file"])
            self.update_play_button()
        else:
            self.show_message("Demo Track", f"Playing: {track['name']} by {track['artist']}\n\nNo audio file found.")
    
    def toggle_play(self):
        if self.current_track_info["name"]:
            track = self.available_tracks[self.current_track_index]
            if track["file"] and os.path.exists(track["file"]):
                self.music_player.play(track["file"])  # This will toggle pause if already playing
                self.update_play_button()
    
    def update_play_button(self):
        if self.music_player.is_playing():
            self.play_button.configure(text="⏸")
        else:
            self.play_button.configure(text="▶")
    
    def next_track(self):
        if self.available_tracks:
            next_index = (self.current_track_index + 1) % len(self.available_tracks)
            self.play_track(self.available_tracks[next_index], next_index)
    
    def previous_track(self):
        if self.available_tracks:
            prev_index = (self.current_track_index - 1) % len(self.available_tracks)
            self.play_track(self.available_tracks[prev_index], prev_index)
    
    def forward_10(self):
        self.music_player.forward()
    
    def backward_10(self):
        self.music_player.backward()
    
    def set_volume(self, value):
        self.music_player.set_volume(value)
    
    def show_message(self, title, message):
        message_window = ctk.CTkToplevel(self)
        message_window.title(title)
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
    app = DemoMusicApp()
    app.mainloop()