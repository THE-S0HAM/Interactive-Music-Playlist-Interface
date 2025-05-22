import customtkinter as ctk
from app import MusicPlaylistApp

if __name__ == "__main__":
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run the application
    app = MusicPlaylistApp()
    app.mainloop()