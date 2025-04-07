# YouTube Video Transcription App Documentation

## Project Overview
A Streamlit-based application for transcribing YouTube videos with support for single videos, multiple videos, and playlists. The app features a modern UI with video previews and flexible transcript generation options.

## Key Features
- Single video transcription
- Multiple video batch processing
- Playlist processing with video preview
- YouTube-like grid interface for playlist videos
- Flexible language selection (English/French)
- Custom save location selection
- Progress tracking
- Timestamp preservation in transcripts

## Technical Implementation

### Core Components
1. **YouTube Integration**
   - Initially used `pytube`, later switched to `pytubefix` for better reliability
   - Handles video metadata fetching (titles, durations, thumbnails)
   - Manages playlist processing

2. **Transcript Processing**
   - Uses `youtube_transcript_api` for fetching captions
   - Handles both short and long videos
   - Preserves timing information in output

3. **UI Components**
   - Built with Streamlit
   - Responsive grid layout for videos
   - Progress indicators
   - Session state management

## Challenges & Solutions

### 1. Video Title Fetching
**Problem**: HTTP 400 errors when fetching video metadata
**Solutions**:
- Switched from `pytube` to `pytubefix`
- Implemented rate limiting
- Added better error handling
- Fallback to video ID when title fetch fails

### 2. Transcript Format
**Problem**: FetchedTranscriptSnippet objects not directly writable
**Solution**:
- Added proper object handling
- Implemented custom formatting
- Preserved timestamp information
- Added structured text output

### 3. UI/UX Improvements
**Problem**: Basic interface needed enhancement
**Solutions**:
- Added grid layout for playlist videos
- Implemented YouTube-like preview cards
- Added progress bars
- Improved button placement
- Fixed vertical alignment issues

### 4. Session State Management
**Problem**: Streamlit session state conflicts
**Solutions**:
- Properly initialized session state
- Fixed state update timing
- Implemented proper rerun mechanisms
- Added clear selection functionality

## Code Structure
```
e:\transcriber\
├── app.py              # Main application
├── video_preview.py    # Video UI components
├── transcribe.py       # Transcription logic
└── requirements.txt    # Dependencies
```

## Dependencies
- `streamlit`: UI framework
- `pytubefix`: YouTube video handling
- `youtube-transcript-api`: Transcript fetching
- `tk`: File dialog functionality
- Additional utilities for formatting and file handling

## Future Improvements
1. Add support for more languages
2. Add transcript preview before saving
3. Support for custom timestamp formats
4. Add batch download progress tracking
5. Implement error recovery for failed downloads
6. Add support for subtitle translation

## Usage Instructions
1. **Single Video Transcription**
   - Paste video URL
   - Select language
   - Choose save location
   - Click "Start Transcription"

2. **Multiple Videos**
   - Enter URLs (one per line)
   - Select common language
   - Choose save location
   - Process all videos

3. **Playlist Processing**
   - Enter playlist URL
   - Preview and select videos
   - Choose language and save location
   - Process selected videos

## Error Handling
- Invalid URLs: Proper error messages
- Missing transcripts: Warning messages
- Network issues: Retry mechanism
- File system errors: Clear error reporting
- Invalid save locations: User feedback

## Performance Considerations
- Rate limiting for API calls
- Batch processing optimization
- Progress tracking for long operations
- Memory efficient video handling
- Proper resource cleanup
