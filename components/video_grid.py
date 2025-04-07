import streamlit as st
from typing import List, Set, Dict
from datetime import timedelta

def format_duration(seconds: int) -> str:
    """Format duration as HH:MM:SS or MM:SS."""
    return str(timedelta(seconds=seconds))[2:] if seconds < 3600 else str(timedelta(seconds=seconds))

def show_video_grid(videos: List[Dict], selected_videos: Set[str], cols: int = 3):
    """
    Display videos in a responsive grid layout.
    
    Args:
        videos: List of video metadata
        selected_videos: Set of selected video IDs
        cols: Number of grid columns
    """
    # Calculate dimensions
    card_width = min(300, int(1200/cols))
    thumbnail_width = card_width - 20

    # Create grid
    for i in range(0, len(videos), cols):
        with st.container():
            row = st.columns(cols)
            for col_idx, video in enumerate(videos[i:i+cols]):
                if col_idx < len(row):
                    with row[col_idx]:
                        _render_video_card(video, thumbnail_width, selected_videos)

def _render_video_card(video: Dict, width: int, selected_videos: Set[str]):
    """Render individual video card."""
    with st.container():
        # Thumbnail
        st.image(video['thumbnail_url'], width=width)
        
        # Title
        title = video['title'][:57] + "..." if len(video['title']) > 60 else video['title']
        st.markdown(f"<h4 style='margin:5px 0;font-size:14px'>{title}</h4>", unsafe_allow_html=True)
        
        # Duration and controls
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(
                f"<p style='color:#606060;font-size:12px'>{format_duration(video['duration'])}</p>",
                unsafe_allow_html=True
            )
        with col2:
            _render_control_buttons(video, selected_videos)
        
        # Preview button
        st.link_button("▶ Preview", video['url'], use_container_width=True)

def _render_control_buttons(video: Dict, selected_videos: Set[str]):
    """Render Add/Remove buttons."""
    button_key = f"toggle_{video['id']}"
    if video['id'] in selected_videos:
        if st.button("Remove", key=button_key, type="secondary", use_container_width=True):
            selected_videos.remove(video['id'])
            st.session_state[button_key] = False
    else:
        if st.button("Add", key=button_key, use_container_width=True):
            selected_videos.add(video['id'])
            st.session_state[button_key] = True
