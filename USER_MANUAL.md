# YouTube Transcription App - User Manual

## Overview
This application helps you download transcripts from YouTube videos. It supports single videos, multiple videos, and entire playlists. You can get transcripts in their original language or translate them to other supported languages.

## Features
- Download transcripts from single videos
- Process multiple videos at once
- Select videos from playlists with preview
- Choose between different languages
- Translate transcripts
- Save with timestamps
- Browse local folders

### Using the App

#### Single Video Transcription
1. Select "Single Video" option
2. Paste the YouTube video URL
3. Choose save location using Browse button
4. Select source language (language of the video)
5. (Optional) Select target language for translation
6. Click "Start Transcription"

#### Multiple Videos
1. Select "Multiple Videos" option
2. Enter one YouTube URL per line
3. Choose save location
4. Select languages
5. Click "Start Transcription"

#### Playlist Processing
1. Select "Playlist" option
2. Paste the playlist URL
3. Click "Load Playlist" to see videos
4. Select videos you want to transcribe
5. Choose save location and languages
6. Click "Start Transcription"

### Language Options
- Source Language: Original language of the video
- Target Language: Language to translate to (optional)
- Supported languages:
  - English (en)
  - French (fr)
  - Spanish (es)
  - German (de)
  - Italian (it)

### Output Format
Transcripts are saved as text files with timestamps:
```
[00:00:05 → 00:00:08] This is an example transcript
[00:00:08 → 00:00:12] With timestamps for each segment
```

## Troubleshooting

### Common Issues

1. **"No transcript available"**
   - Video might not have closed captions
   - Try different source language
   - Check if video is public

2. **"Failed to load playlist"**
   - Verify playlist is public
   - Check internet connection
   - Try pasting URL again

3. **"Invalid YouTube URL format"**
   - Use complete YouTube URLs
   - Remove any extra parameters

4. **"Failed to process video"**
   - Wait a few minutes and try again
   - Check if video is still available
   - Verify language selection

### Tips
- Use "Clear Selection" to reset playlist choices
- Browse button helps avoid path typing errors
- Wait for playlist to fully load before selecting videos
- For long videos, processing may take a few minutes
- Keep internet connection stable during processing

## Limitations
- Requires videos to have closed captions
- Translation quality depends on source transcript
- Processing time varies with video length
- Some videos may have restricted transcripts
- Playlist must be public or unlisted
