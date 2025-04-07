import streamlit as st
from utils.file_utils import sanitize_filename, format_transcript_content, create_zip_content
from utils.youtube_utils import extract_video_id, get_video_metadata
from components.video_grid import show_video_grid
from utils.transcription import get_transcript
from typing import List, Dict, Set

# Initialize session states
if 'selected_videos' not in st.session_state:
    st.session_state['selected_videos'] = set()
if 'playlist_videos' not in st.session_state:
    st.session_state['playlist_videos'] = []
if 'processed_transcripts' not in st.session_state:
    st.session_state['processed_transcripts'] = {}
if 'processed_videos' not in st.session_state:
    st.session_state['processed_videos'] = []

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

def process_transcription(video_ids: List[str], source_lang: str, target_lang: str):
    """Process transcription for selected videos."""
    if not video_ids:
        st.warning("Please select videos to transcribe")
        return

    progress_bar = st.progress(0)
    newly_processed = []
    
    for idx, video_id in enumerate(video_ids):
        try:
            metadata = next(v for v in st.session_state['playlist_videos'] 
                          if v['id'] == video_id)
            st.write(f"Processing video: {metadata['title']}")
            
            # Check if already processed
            existing = next((v for v in st.session_state['processed_videos'] 
                           if v['id'] == video_id), None)
            if existing:
                newly_processed.append(existing)
            else:
                transcript = get_transcript(video_id, source_lang, target_lang)
                if transcript:
                    content = format_transcript_content(transcript)
                    filename = f"{sanitize_filename(metadata['title'])}.txt"
                    video_data = {
                        'id': video_id,
                        'title': metadata['title'],
                        'content': content,
                        'filename': filename
                    }
                    newly_processed.append(video_data)
                    if video_data not in st.session_state['processed_videos']:
                        st.session_state['processed_videos'].append(video_data)
                else:
                    st.warning(f"No transcript available for: {metadata['title']}")
            
            progress_bar.progress((idx + 1) / len(video_ids))
        except Exception as e:
            st.warning(f"Failed to process video {video_id}: {str(e)}")
    
    progress_bar.empty()
    display_processed_videos()

def display_processed_videos():
    """Display processed videos with appropriate download options."""
    if not st.session_state['processed_videos']:
        return
        
    st.header("Download Transcripts")
    
    # Single video - direct download
    if len(st.session_state['processed_videos']) == 1:
        video = st.session_state['processed_videos'][0]
        st.download_button(
            label="📥 Download Transcript",
            data=video['content'],
            file_name=video['filename'],
            mime="text/plain",
            key=f"dl_{video['id']}"
        )
        
    # Multiple videos - zip download
    else:
        # Show individual download buttons
        for video in st.session_state['processed_videos']:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(video['title'])
                with col2:
                    st.download_button(
                        label="📥",
                        data=video['content'],
                        file_name=video['filename'],
                        mime="text/plain",
                        key=f"dl_{video['id']}_{hash(video['content'])}"
                    )
        
        # Add zip download option
        st.divider()
        zip_data, zip_name = create_zip_content(st.session_state['processed_videos'])
        st.download_button(
            label="📥 Download All Transcripts as ZIP",
            data=zip_data,
            file_name=zip_name,
            mime="application/zip",
            key="download_all_zip",
            use_container_width=True
        )

def process_single_video(video_id: str, source_lang: str, target_lang: str):
    """Handle single video transcription."""
    try:
        metadata = get_video_metadata(video_id)
        if not metadata:
            raise Exception("Could not fetch video metadata")
            
        st.write(f"Processing video: {metadata['title']}")
        
        # Check if already processed
        existing = next((v for v in st.session_state['processed_videos'] 
                        if v['id'] == video_id), None)
        if existing:
            video_data = existing
        else:
            transcript = get_transcript(video_id, source_lang, target_lang)
            if transcript:
                content = format_transcript_content(transcript)
                filename = f"{sanitize_filename(metadata['title'])}.txt"
                video_data = {
                    'id': video_id,
                    'title': metadata['title'],
                    'content': content,
                    'filename': filename
                }
                st.session_state['processed_videos'].append(video_data)
            else:
                st.warning(f"No transcript available for this video")
                return
        
        display_processed_videos()
        st.success(f"Transcript ready for: {metadata['title']}")
            
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

# Language selection
st.header("Language Options")
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source language:", ["fr", "en", "auto"])
with col2:
    target_lang = st.selectbox("Target language (optional):", ["", "fr", "en", "es", "de", "it"])

# Process button
if st.button("Start Transcription"):
    if not link:
        st.error("Please provide a video or playlist link.")
    else:
        if link_type == "Single Video":
            video_id = extract_video_id(link)
            process_single_video(video_id, source_lang, target_lang)
        elif link_type == "Multiple Videos":
            video_ids = [extract_video_id(l) for l in link.splitlines() if l.strip()]
            process_transcription(video_ids, source_lang, target_lang)
        elif link_type == "Playlist":
            process_transcription(list(st.session_state['selected_videos']), source_lang, target_lang)
