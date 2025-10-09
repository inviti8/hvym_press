import os
import urllib.parse
from pathlib import Path

def normalize_path(path):
    """Convert path to use forward slashes and normalize it."""
    return str(Path(path).resolve().as_posix())

def url_to_path(base_dir, url_path):
    """Convert URL path to filesystem path, handling Windows paths."""
    # Decode URL-encoded characters
    path = urllib.parse.unquote(url_path)
    
    # Remove leading slash if present
    if path.startswith('/'):
        path = path[1:]
    
    # Join with base directory and normalize
    full_path = os.path.join(base_dir, path.replace('/', os.sep))
    return normalize_path(full_path)

def ensure_directory(path):
    """Ensure the directory exists, create if it doesn't."""
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    return path
