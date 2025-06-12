"""
Main entry point for the revamped Music Playlist Interface
"""
import customtkinter as ctk
from revamped_app import RevampedMusicApp
from modern_theme import setup_modern_theme

if __name__ == "__main__":
    # Apply modern theme
    setup_modern_theme()
    
    # Create and run the application
    app = RevampedMusicApp()
    app.mainloop()