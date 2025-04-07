# YouTube Transcript Extractor

A simple Python application for extracting and translating YouTube video transcripts with a modern Streamlit interface. This tool supports single videos, multiple videos, and playlist processing with advanced language options and timestamp preservation.

## Introduction

The YouTube Transcript Extractor addresses the challenge of obtaining high-quality transcripts from YouTube videos at scale. Built with Streamlit and modern Python libraries, it provides an intuitive interface for managing transcript extraction tasks while handling various edge cases and language requirements.

## Core Functionality

The application excels at processing YouTube content in three primary modes. The single video mode allows for quick transcript extraction from individual videos with optional translation. The multiple videos mode enables batch processing of unrelated videos. The playlist mode offers a visual interface for selecting and processing videos from YouTube playlists, complete with thumbnails and duration information.

## Technical Architecture

At its core, the application utilizes PyTubeFix for reliable YouTube data extraction and youtube-transcript-api for accessing closed captions. The translation functionality is powered by the deep-translator library, enabling cross-language transcript generation. State management is handled through Streamlit's session state, ensuring a seamless user experience across interactions.

## Installation Requirements

The application requires Python 3.8 or newer and depends on several key packages:
```bash
python -m pip install -r requirements.txt
```

The requirements include streamlit for the user interface, pytubefix for YouTube integration, youtube-transcript-api for transcript access, and additional utilities for text processing and file management.

## Usage Instructions

Launch the application using Streamlit:
```bash
streamlit run app.py
```

The interface presents three workflow options: single video processing, multiple video batch processing, and playlist management. Each mode offers appropriate controls for language selection, output location, and processing options. The application automatically handles rate limiting and provides progress feedback during lengthy operations.

## Cloud Deployment

When deploying to Streamlit Cloud:
1. The application uses simple path input instead of system file picker
2. Ensure the save path exists and is writable
3. You may need to create the output directory before running

## Error Handling & Reliability

Robust error handling ensures graceful operation even when encountering common issues like unavailable transcripts, network problems, or rate limiting. The application implements automatic retries with exponential backoff, falls back to alternative transcript sources when necessary, and provides clear feedback about any issues encountered during processing.

## Output Format

Transcripts are saved as formatted text files with precise timestamps, making them suitable for various downstream applications. The timestamp format follows the standard [HH:MM:SS] convention, and translations maintain the original timing information. All output is UTF-8 encoded to preserve special characters across languages.

## Development & Extension

The modular architecture facilitates easy extension and modification. Core functionality is organized into logical modules:
- utils/: Contains transcript processing, file management, and YouTube interaction utilities
- components/: Houses reusable UI components and layouts
- app.py: Main application entry point and UI orchestration

## Performance Considerations

The application implements several optimizations for handling large playlists and long videos:
- Batch processing with progress tracking
- Memory-efficient transcript handling
- Rate limiting to prevent API throttling
- Caching of video metadata
- Efficient state management

## Support & Troubleshooting

Common issues are documented in the USER_MANUAL.md file, which provides detailed troubleshooting steps. Most problems can be resolved by:
1. Verifying video/playlist accessibility
2. Checking for available closed captions
3. Ensuring stable internet connectivity
4. Validating language selection
5. Confirming write permissions in the output directory

## License & Acknowledgments

This project is released under the MIT License. It builds upon several open-source projects and the YouTube Data API. Special thanks to the maintainers of pytube, youtube-transcript-api, and the Streamlit community for their invaluable contributions.
