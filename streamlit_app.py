import streamlit as st
import os
from utils.file_utils import sanitize_filename, validate_save_location, select_folder
from utils.youtube_utils import extract_video_id, get_video_metadata, fetch_transcript
from components.video_grid import show_video_grid
from utils.transcription import get_transcript, save_transcript_with_timestamps
from typing import List, Dict, Set
import time

# Initialize session states
if 'folder_path' not in st.session_state:
    st.session_state['folder_path'] = ''
if 'selected_videos' not in st.session_state:
    st.session_state['selected_videos'] = set()
if 'playlist_videos' not in st.session_state:
    st.session_state['playlist_videos'] = []

def load_playlist():
    """Load and process playlist videos."""
    playlist_url = st.session_state.get('playlist_url', '')
    if playlist_url:
        with st.spinner("Loading playlist videos..."):
            try:
                from pytubefix import Playlist
                playlist = Playlist(playlist_url)
                videos = []
                
                progress_bar = st.progress(0)
                for idx, video_url in enumerate(playlist.video_urls):
                    video_id = extract_video_id(video_url)
                    metadata = get_video_metadata(video_id)
                    if metadata:
                        videos.append(metadata)
                    progress = (idx + 1) / len(playlist.video_urls)
                    progress_bar.progress(progress)
                
                st.session_state['playlist_videos'] = videos
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load playlist: {str(e)}")

def process_transcription(video_ids: List[str], save_folder: str, source_lang: str, target_lang: str):
    """Process transcription for selected videos."""
    if not video_ids:
        st.warning("Please select videos to transcribe")
        return

    progress_bar = st.progress(0)
    for idx, video_id in enumerate(video_ids):
        try:
            # Get video metadata
            metadata = next(v for v in st.session_state['playlist_videos'] 
                          if v['id'] == video_id)
            st.write(f"Processing video: {metadata['title']}")
            
            # Fetch and save transcript
            transcript = get_transcript(video_id, source_lang, target_lang)
            if transcript:
                save_path = os.path.join(save_folder, f"{sanitize_filename(metadata['title'])}.txt")
                save_transcript_with_timestamps(transcript, save_path)
                st.success(f"Saved transcript for: {metadata['title']}")
            else:
                st.warning(f"No transcript available for: {metadata['title']}")
            
            progress_bar.progress((idx + 1) / len(video_ids))
        except Exception as e:
            st.warning(f"Failed to process video {video_id}: {str(e)}")
    
    progress_bar.empty()

def process_single_video(video_id: str, save_folder: str, source_lang: str, target_lang: str):
    """Handle single video transcription with proper metadata handling."""
    try:
        # Get video metadata
        metadata = get_video_metadata(video_id)
        if not metadata:
            raise Exception("Could not fetch video metadata")
            
        st.write(f"Processing video: {metadata['title']}")
        
        # Fetch and save transcript
        transcript = get_transcript(video_id, source_lang, target_lang)
        if transcript:
            save_path = os.path.join(save_folder, f"{sanitize_filename(metadata['title'])}.txt")
            save_transcript_with_timestamps(transcript, save_path)
            st.success(f"Saved transcript for: {metadata['title']}")
        else:
            st.warning(f"No transcript available for this video")
            
    except Exception as e:
        st.error(f"Failed to process video {video_id}: {str(e)}")

# UI Layout
st.title("YouTube Video Transcription App")

# Input for video or playlist link
st.header("Input Video or Playlist Link")
link_type = st.radio("Select the type of link:", ["Single Video", "Multiple Videos", "Playlist"])

if link_type == "Multiple Videos":
    link = st.text_area("Enter video links (one per line):", height=150)
elif link_type == "Playlist":
    col1, col2 = st.columns([4, 1])
    with col1:
        link = st.text_input("Enter playlist URL:", key='playlist_url')
    with col2:
        st.write("")
        if st.button("Load Playlist", type="primary"):
            load_playlist()
    
    # Show playlist videos in grid
    if st.session_state['playlist_videos']:
        # Show selected count and clear selection button
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_count = len(st.session_state['selected_videos'])
            st.subheader(f"Playlist Videos ({selected_count} selected)")
        with col2:
            if selected_count > 0 and st.button("Clear Selection"):
                st.session_state['selected_videos'].clear()
                st.rerun()
        
        # Display videos in grid
        show_video_grid(st.session_state['playlist_videos'], st.session_state['selected_videos'])
else:
    link = st.text_input("Enter the link:")

# Input for local folder to save transcripts
st.header("Save Location")
save_folder = st.text_input("Enter the path where transcripts will be saved:")

if not save_folder:
    st.info("Please enter a folder path to save transcripts")
elif not os.path.exists(save_folder):
    st.error("The specified folder does not exist")
elif not os.access(save_folder, os.W_OK):
    st.error("Cannot write to the specified folder. Please check permissions")

# Input for language selection
st.header("Language Options")
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source language:", ["fr", "en", "auto"])
with col2:
    target_lang = st.selectbox("Target language (optional):", ["", "fr", "en", "es", "de", "it"])

# Process button
if st.button("Start Transcription"):
    if not link or not save_folder:
        st.error("Please provide both the link(s) and the save folder.")
    elif not os.path.exists(save_folder):
        st.error("The specified folder does not exist. Please provide a valid folder path.")
    else:
        if link_type == "Single Video":
            video_id = extract_video_id(link)
            process_single_video(video_id, save_folder, source_lang, target_lang)
        elif link_type == "Multiple Videos":
            video_ids = [extract_video_id(l) for l in link.splitlines() if l.strip()]
            process_transcription(video_ids, save_folder, source_lang, target_lang)
        elif link_type == "Playlist":
            process_transcription(list(st.session_state['selected_videos']), save_folder, source_lang, target_lang)
