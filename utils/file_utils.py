import re
import io
import zipfile

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

def create_zip_content(videos: list) -> tuple[bytes, str]:
    """
    Create a zip file containing multiple transcripts.
    
    Args:
        videos: List of processed video data
    Returns:
        Tuple of (zip_bytes, filename)
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for video in videos:
            zip_file.writestr(video['filename'], video['content'])
    
    return zip_buffer.getvalue(), "transcripts.zip"
