# Simple YouTube Downloader

A simple console menu program for downloading YouTube videos, implemented using [PyTubeFix](https://github.com/JuanBindez/pytubefix).

## Features

- Text-based User Interface.
- Download:
  - Video with audio (with options).
  - Video only (with options).
  - Audio only (with options).
  - Captions for any available languages (includes auto-generated caption).
  - Thumbnails.

## Prerequisites

- Python >= 3.12.
- FFMPEG is required for merging video and audio files.
- Packages used: [PyTubeFix](https://github.com/JuanBindez/pytubefix), requests, tqdm.

## Installation

1. **Install any [Python >= 3.12](https://www.python.org/downloads/).**
2. **Install [FFMPEG](https://www.ffmpeg.org/download.html).**

    After installation, ensure that `ffmpeg` is accessible from your system's PATH. You can verify this by running `ffmpeg -version` in your terminal.

3. **Clone this repo to your device:**

    ```bash
    git clone https://github.com/dungvd0309/simple-youtube-downloader
    ```

4. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

## How to run

Run `main.py` in your terminal:

```bash
python main.py
```
