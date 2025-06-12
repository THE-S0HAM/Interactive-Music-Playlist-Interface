"""
Cleanup script to remove unnecessary files from the repository
"""
import os
import shutil

# Files to keep (essential files for the revamped version)
KEEP_FILES = [
    'LICENCE',
    'README.md',
    'requirements.txt',
    'config.json',
    '.gitignore',
    'revamped_main.py',
    'revamped_app.py',
    'modern_theme.py',
    'player.py',
    'playlist_manager.py',
    'analytics.py',
    'spotify_auth.py',
    'ui_components.py',
    'cleanup.py'  # This script
]

# Directories to keep
KEEP_DIRS = [
    'sample_tracks',
    '.cache'  # Spotify auth cache
]

def cleanup_repository(repo_path):
    """Remove unnecessary files from the repository"""
    print(f"Cleaning up repository at: {repo_path}")
    
    # Get all files and directories in the repository
    all_items = os.listdir(repo_path)
    
    for item in all_items:
        item_path = os.path.join(repo_path, item)
        
        # Skip directories we want to keep
        if os.path.isdir(item_path) and item in KEEP_DIRS:
            print(f"Keeping directory: {item}")
            continue
        
        # Skip files we want to keep
        if os.path.isfile(item_path) and item in KEEP_FILES:
            print(f"Keeping file: {item}")
            continue
        
        # Remove everything else
        try:
            if os.path.isdir(item_path):
                print(f"Removing directory: {item}")
                shutil.rmtree(item_path)
            else:
                print(f"Removing file: {item}")
                os.remove(item_path)
        except Exception as e:
            print(f"Error removing {item}: {str(e)}")
    
    print("Cleanup complete!")

if __name__ == "__main__":
    # Get the repository path (current directory)
    repo_path = os.path.dirname(os.path.abspath(__file__))
    
    # Confirm before proceeding
    print("This script will remove all files except those needed for the revamped version.")
    print("Files to keep:", ", ".join(KEEP_FILES))
    print("Directories to keep:", ", ".join(KEEP_DIRS))
    
    confirm = input("Do you want to proceed? (y/n): ")
    if confirm.lower() == 'y':
        cleanup_repository(repo_path)
    else:
        print("Cleanup cancelled.")