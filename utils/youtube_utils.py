from typing import Optional, Dict, List
import time
from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    raise ValueError("Invalid YouTube URL format")

def get_video_metadata(video_id: str, retry_count: int = 2) -> Optional[Dict]:
    """
    Fetch video metadata with retry mechanism.
    
    Args:
        video_id: YouTube video ID
        retry_count: Number of retries on failure
    Returns:
        Dictionary containing video metadata
    """
    for attempt in range(retry_count):
        try:
            time.sleep(1)  # Rate limiting
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            return {
                'id': video_id,
                'title': yt.title,
                'duration': yt.length,
                'thumbnail_url': yt.thumbnail_url,
                'url': yt.watch_url
            }
        except Exception as e:
            if attempt == retry_count - 1:
                raise e
            time.sleep(2)  # Longer delay before retry
    return None

def fetch_transcript(video_id: str, language: str = 'en') -> List[Dict]:
    """
    Fetch and format video transcript.
    
    Args:
        video_id: YouTube video ID
        language: Transcript language code
    Returns:
        List of transcript segments with timing
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language])
        return [
            {
                'text': entry.text,
                'start': entry.start,
                'duration': entry.duration
            }
            for entry in transcript.fetch()
        ]
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")
