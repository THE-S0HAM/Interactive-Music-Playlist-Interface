"""
Reusable UI components for the Music Playlist Interface
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os

class GradientFrame(ctk.CTkFrame):
    """A frame with a gradient background"""
    def __init__(self, master, start_color, end_color, **kwargs):
        super().__init__(master, **kwargs)
        self.start_color = start_color
        self.end_color = end_color
        self.bind("<Configure>", self._create_gradient)
        
    def _create_gradient(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Create gradient image
        gradient_img = Image.new('RGBA', (width, height), color=0)
        
        # Generate gradient
        for y in range(height):
            r_ratio = y / height
            r = int((1 - r_ratio) * int(self.start_color[1:3], 16) + r_ratio * int(self.end_color[1:3], 16))
            g = int((1 - r_ratio) * int(self.start_color[3:5], 16) + r_ratio * int(self.end_color[3:5], 16))
            b = int((1 - r_ratio) * int(self.start_color[5:7], 16) + r_ratio * int(self.end_color[5:7], 16))
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            line = Image.new('RGBA', (width, 1), color=color)
            gradient_img.paste(line, (0, y))
        
        # Convert to PhotoImage and keep reference
        self.gradient = ImageTk.PhotoImage(gradient_img)
        self.create_image(0, 0, anchor="nw", image=self.gradient)

class MusicCard(ctk.CTkFrame):
    """Card component for displaying music items"""
    def __init__(self, master, title, subtitle, image_path=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure frame
        self.configure(corner_radius=10, fg_color="#1E1E1E")
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        
        # Album art (placeholder if no image)
        if image_path and os.path.exists(image_path):
            self.image = ctk.CTkImage(light_image=Image.open(image_path),
                                     dark_image=Image.open(image_path),
                                     size=(60, 60))
        else:
            # Create placeholder
            placeholder = Image.new('RGB', (60, 60), color="#333333")
            self.image = ctk.CTkImage(light_image=placeholder,
                                     dark_image=placeholder,
                                     size=(60, 60))
        
        self.image_label = ctk.CTkLabel(self, image=self.image, text="")
        self.image_label.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10)
        
        # Title
        self.title_label = ctk.CTkLabel(self, text=title, 
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.title_label.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="w")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self, text=subtitle, 
                                          font=ctk.CTkFont(size=12))
        self.subtitle_label.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="w")

class AnimatedButton(ctk.CTkButton):
    """Button with hover animation"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.original_color = self.cget("fg_color")
        self.hover_color = self.cget("hover_color")
        
        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event):
        self.configure(fg_color=self.hover_color)
        
    def _on_leave(self, event):
        self.configure(fg_color=self.original_color)

class SearchBar(ctk.CTkFrame):
    """Custom search bar with icon"""
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure frame
        self.configure(corner_radius=20, fg_color="#2A2A2A", height=40)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search...", 
                                        border_width=0, fg_color="transparent")
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(15, 5), pady=5)
        
        # Search button
        self.search_button = ctk.CTkButton(self, text="Search", width=80, height=30,
                                          command=lambda: command(self.search_entry.get()) if command else None)
        self.search_button.pack(side="right", padx=5, pady=5)

class ScrollableCardFrame(ctk.CTkScrollableFrame):
    """Frame for displaying cards in a scrollable container"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
    def add_card(self, title, subtitle, image_path=None, command=None):
        """Add a card to the frame"""
        card = MusicCard(self, title, subtitle, image_path)
        card.pack(fill="x", padx=10, pady=5)
        
        if command:
            card.bind("<Button-1>", lambda e: command())
            
        return card