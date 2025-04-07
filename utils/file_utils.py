import os
import re

def sanitize_filename(title: str, max_length: int = 100) -> str:
    """
    Sanitize filename by removing invalid characters and limiting length.
    
    Args:
        title: Raw filename
        max_length: Maximum allowed length
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    return sanitized[:max_length]

def validate_save_location(path: str) -> bool:
    """
    Validate if save location exists and is writable.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return os.path.exists(path) and os.access(path, os.W_OK)
    except:
        return False

def select_folder(initial_dir: str = None) -> str:
    """
    Cloud-compatible folder selection.
    For cloud deployment, this just returns the input path or a default.
    
    Args:
        initial_dir: Initial directory path
    Returns:
        Selected directory path
    """
    # For cloud deployment, we'll just use the provided path or a default
    if initial_dir and os.path.exists(initial_dir):
        return initial_dir
    
    # Default to a directory that should be writable in cloud environment
    return os.path.join(os.path.expanduser('~'), 'transcripts')
