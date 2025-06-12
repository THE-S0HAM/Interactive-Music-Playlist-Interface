"""
Simple music player for Spotify previews
"""
import os
import tempfile
import threading
import webbrowser
import requests
import pygame

class MusicPlayer:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        self.currently_playing = None
        self.temp_files = []
    
    def play(self, url=None, track_id=None):
        """Play a track from URL or open in Spotify"""
        # Stop any currently playing music
        self.stop()
        
        # If no preview URL but we have track ID, open in Spotify
        if not url and track_id:
            spotify_url = f"https://open.spotify.com/track/{track_id}"
            webbrowser.open(spotify_url)
            return True, "Opening in Spotify"
        
        # If no preview URL and no track ID
        if not url:
            return False, "No playable source available"
            
        try:
            # Download the preview file to a temporary location
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_file.write(response.content)
                temp_file.close()
                
                # Keep track of the file for cleanup
                self.temp_files.append(temp_file.name)
                self.currently_playing = temp_file.name
                
                # Play the music
                pygame.mixer.music.load(temp_file.name)
                pygame.mixer.music.play()
                
                # Start a thread to clean up when done
                threading.Thread(target=self._monitor_playback, args=(temp_file.name,)).start()
                
                return True, "Playing preview"
            else:
                # Fallback to Spotify if download fails
                if track_id:
                    spotify_url = f"https://open.spotify.com/track/{track_id}"
                    webbrowser.open(spotify_url)
                    return True, "Opening in Spotify (download failed)"
                return False, f"Failed to download preview: HTTP {response.status_code}"
        except Exception as e:
            # Fallback to Spotify if there's an error
            if track_id:
                spotify_url = f"https://open.spotify.com/track/{track_id}"
                webbrowser.open(spotify_url)
                return True, "Opening in Spotify (error occurred)"
            return False, f"Error playing preview: {str(e)}"
    
    def stop(self):
        """Stop any currently playing music"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    
    def _monitor_playback(self, filename):
        """Monitor playback and clean up when done"""
        # Wait until the music is no longer playing
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)  # Check every second
        
        # Clean up the file if it's no longer needed
        if filename == self.currently_playing:
            self.currently_playing = None
        
        # Delete the file if it exists
        try:
            if os.path.exists(filename):
                os.unlink(filename)
                if filename in self.temp_files:
                    self.temp_files.remove(filename)
        except:
            pass  # Ignore errors in cleanup
    
    def cleanup(self):
        """Clean up all temporary files"""
        self.stop()
        for file in self.temp_files:
            try:
                if os.path.exists(file):
                    os.unlink(file)
            except:
                pass
        self.temp_files = []