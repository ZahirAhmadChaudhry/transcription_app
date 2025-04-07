import os
import re
import tkinter as tk
from tkinter import filedialog

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

def select_folder() -> str:
    """
    Open system folder selection dialog.
    Returns:
        Selected folder path or empty string
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path

def validate_save_location(path: str) -> bool:
    """
    Validate if save location exists and is writable.
    """
    return os.path.exists(path) and os.access(path, os.W_OK)
