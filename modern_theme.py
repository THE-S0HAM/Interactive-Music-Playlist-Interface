"""
Modern theme configuration for the revamped Music Playlist Interface
"""
import customtkinter as ctk

# Vibrant Color Palette
DARK_BG = "#121212"  # Deep black background
DARK_CARD_BG = "#1E1E1E"  # Slightly lighter black for cards
PRIMARY_COLOR = "#8A2BE2"  # Vibrant purple
SECONDARY_COLOR = "#00C9FF"  # Bright cyan
ACCENT_COLOR = "#FF4081"  # Hot pink accent
SUCCESS_COLOR = "#00E676"  # Bright green
WARNING_COLOR = "#FFAB00"  # Amber
ERROR_COLOR = "#FF5252"  # Red
TEXT_COLOR = "#FFFFFF"  # White text
SUBTEXT_COLOR = "#B3B3B3"  # Light gray for secondary text

# Light Mode Colors
LIGHT_BG = "#F5F5F5"  # Light gray background
LIGHT_CARD_BG = "#FFFFFF"  # White for cards
LIGHT_PRIMARY = "#6200EA"  # Deep purple
LIGHT_SECONDARY = "#0091EA"  # Blue
LIGHT_TEXT = "#212121"  # Near black text
LIGHT_SUBTEXT = "#757575"  # Medium gray for secondary text

def setup_modern_theme():
    """Apply the modern theme to customtkinter"""
    # Set default appearance mode
    ctk.set_appearance_mode("dark")
    
    # Create custom theme
    ctk.set_default_color_theme("blue")  # Base theme
    
    # Override with our vibrant colors
    ctk.ThemeManager.theme["CTk"]["fg_color"] = [LIGHT_BG, DARK_BG]
    ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = [LIGHT_CARD_BG, DARK_CARD_BG]
    
    # Buttons
    ctk.ThemeManager.theme["CTkButton"]["fg_color"] = [LIGHT_PRIMARY, PRIMARY_COLOR]
    ctk.ThemeManager.theme["CTkButton"]["hover_color"] = [LIGHT_SECONDARY, SECONDARY_COLOR]
    ctk.ThemeManager.theme["CTkButton"]["text_color"] = [LIGHT_CARD_BG, TEXT_COLOR]
    ctk.ThemeManager.theme["CTkButton"]["corner_radius"] = 8
    
    # Text elements
    ctk.ThemeManager.theme["CTkLabel"]["text_color"] = [LIGHT_TEXT, TEXT_COLOR]
    ctk.ThemeManager.theme["CTkEntry"]["fg_color"] = [LIGHT_CARD_BG, "#2A2A2A"]
    ctk.ThemeManager.theme["CTkEntry"]["border_color"] = [LIGHT_SECONDARY, SECONDARY_COLOR]
    
    # Interactive elements
    ctk.ThemeManager.theme["CTkSwitch"]["progress_color"] = [LIGHT_SECONDARY, SECONDARY_COLOR]
    ctk.ThemeManager.theme["CTkSwitch"]["button_hover_color"] = [LIGHT_PRIMARY, PRIMARY_COLOR]
    
    # Scrollbar
    ctk.ThemeManager.theme["CTkScrollbar"]["button_color"] = [LIGHT_SECONDARY, SECONDARY_COLOR]
    ctk.ThemeManager.theme["CTkScrollbar"]["button_hover_color"] = [LIGHT_PRIMARY, PRIMARY_COLOR]