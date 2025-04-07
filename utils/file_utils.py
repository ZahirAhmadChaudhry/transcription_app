import re

def sanitize_filename(title: str, max_length: int = 100) -> str:
    """
    Sanitize filename by removing invalid characters and limiting length.
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    return sanitized[:max_length]

def format_transcript_content(transcript: list) -> str:
    """
    Format transcript entries into downloadable text content.
    """
    content = ""
    for entry in transcript:
        timestamp = f"[{entry.get('start'):.2f} → {entry.get('start') + entry.get('duration'):.2f}] "
        content += f"{timestamp}{entry.get('text')}\n"
    return content
