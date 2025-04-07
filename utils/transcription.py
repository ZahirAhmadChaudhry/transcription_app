from typing import List, Dict, Optional
import os
import time
import logging
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_transcript_segment(entry: Dict) -> Dict:
    """Format a transcript segment with proper timing."""
    try:
        # Handle FetchedTranscriptSnippet objects
        if hasattr(entry, 'text'):
            return {
                'text': str(entry.text),
                'start': float(entry.start),
                'duration': float(entry.duration)
            }
        # Handle dictionary objects
        else:
            return {
                'text': str(entry.get('text', '')),
                'start': float(entry.get('start', 0)),
                'duration': float(entry.get('duration', 0))
            }
    except Exception as e:
        raise Exception(f"Failed to process transcript segment: {str(e)}")

def get_transcript(video_id: str, source_lang: str = 'en', target_lang: str = None) -> Optional[List[Dict]]:
    """Fetch transcript with optional translation."""
    attempts = 2
    for attempt in range(attempts):
        try:
            logger.info(f"Fetching transcript for video {video_id} (Attempt {attempt + 1}/{attempts})")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try requested language first
            try:
                transcript = transcript_list.find_transcript([source_lang])
                logger.info(f"Found transcript in requested language: {source_lang}")
            except Exception as lang_error:
                logger.warning(f"Could not find {source_lang} transcript, trying other languages")
                
                # Get all available transcripts
                try:
                    available_transcripts = transcript_list.find_manually_created_transcript()
                except:
                    try:
                        available_transcripts = transcript_list.find_generated_transcript()
                    except:
                        # Try to get any available transcript
                        try:
                            all_transcripts = transcript_list._manually_created_transcripts + transcript_list._generated_transcripts
                            if all_transcripts:
                                available_transcripts = all_transcripts[0]
                            else:
                                raise Exception("No transcripts available")
                        except:
                            raise Exception("Could not find any transcripts")
                
                transcript = available_transcripts
            
            # Process transcript
            result = [process_transcript_segment(entry) for entry in transcript.fetch()]
            logger.info(f"Successfully fetched {len(result)} transcript segments")
            
            # Handle translation if needed
            if target_lang and target_lang != source_lang and target_lang.strip():
                result = translate_transcript(result, target_lang)
                logger.info(f"Translated transcript to {target_lang}")
            
            return result
            
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == attempts - 1:
                raise Exception(f"Failed to fetch transcript: {str(e)}")
            time.sleep(2)
    
    return None

def save_transcript_with_timestamps(transcript: List[Dict], filepath: str):
    """Save transcript with formatted timestamps."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in transcript:
            timestamp = format_timestamp(entry['start'], entry['duration'])
            f.write(f"{timestamp}{entry['text']}\n")

def format_timestamp(start: float, duration: float) -> str:
    """Format timestamp as [HH:MM:SS → HH:MM:SS]."""
    end = start + duration
    start_time = time.strftime('%H:%M:%S', time.gmtime(start))
    end_time = time.strftime('%H:%M:%S', time.gmtime(end))
    return f"[{start_time} → {end_time}] "

def translate_transcript(transcript: List[Dict], target_lang: str) -> List[Dict]:
    """Translate transcript text while preserving timing."""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = []
        
        # Batch translate to avoid rate limits
        batch_size = 10
        for i in range(0, len(transcript), batch_size):
            batch = transcript[i:i+batch_size]
            texts = [entry['text'] for entry in batch]
            translations = translator.translate_batch(texts)
            
            for entry, trans_text in zip(batch, translations):
                translated.append({
                    'text': trans_text,
                    'start': entry['start'],
                    'duration': entry['duration']
                })
            time.sleep(1)  # Rate limiting
            
        return translated
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
