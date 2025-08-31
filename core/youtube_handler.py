from pytubefix import YouTube, Stream, Caption, StreamQuery, CaptionQuery
from menu_template import clear_console, press_to_continue
import os 
import subprocess
import requests


OUTPUT_PATH = "output/"

def create_output_folder():
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

def sanitize_filename(name: str):
    """Remove illegal characters from file name."""
    illegal = '\\/:*?"<>|'
    trans = str.maketrans('', '', illegal)
    name = name.translate(trans)
    return name


def get_video_stream_list(yt: YouTube) -> StreamQuery:
    """Get a :class:`StreamQuery <StreamQuery>` of DASH video streams."""
    ys = yt.streams.filter(is_dash=True, only_video=True)
    return ys


def get_audio_stream_list(yt: YouTube) -> StreamQuery:
    """Get a :class:`StreamQuery <StreamQuery>` of audio streams."""
    ys = yt.streams.filter(is_dash=True, only_audio=True)
    return ys

def get_caption_list(yt: YouTube) -> CaptionQuery:
    """Get a :class:`CaptionQuery <CaptionQuery>`."""
    return yt.captions

def download_video(yt: YouTube, video: Stream, audio: Stream):
    """Download video and audio stream and merge them with ffmpeg."""
    video_path = video.download(filename="video_only.mp4")
    audio_path = audio.download(filename="audio_only.m4a")

    print("Start merging video and audio...")

    title = sanitize_filename(yt.title)
    filepath = f"[{video.resolution}_{video.fps}fps_{audio.abr}] {title}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c", "copy",
        "-movflags", "+faststart",
        filepath
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    os.remove(video_path)
    os.remove(audio_path)

    print(f"Completed. File saved to {os.path.abspath(filepath)}")


def download_video_only(yt: YouTube, stream: Stream):
    """Download .mp4 video from stream."""
    video = stream
    title = sanitize_filename(yt.title)
    create_output_folder()
    video.download( 
        output_path=OUTPUT_PATH,
        filename=f"[{stream.resolution}_{stream.fps}fps] {title}.mp4"
    )


def download_audio_only(yt: YouTube, stream: Stream):
    """Download .m4a audio from stream."""
    audio = stream
    title = sanitize_filename(yt.title)
    create_output_folder()
    audio.download(
        output_path= OUTPUT_PATH,
        filename=f"[{stream.abr}] {title}.m4a"
    )


def download_caption(yt: YouTube, code: str):
    """Download .srt caption."""
    cap: Caption = yt.captions.get(code)
    title = sanitize_filename(yt.title)
    filename = f"[{code}] {title}.srt"
    filepath = f"{OUTPUT_PATH}/{filename}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cap.generate_srt_captions())
    print(f"Download complete! File saved to: {os.path.abspath(filepath)}")


def download_thumbnail(yt: YouTube):
    """Download .jpg thumbnail image."""
    thumbnail_url = f"https://img.youtube.com/vi/{yt.video_id}/maxresdefault.jpg"
    title = sanitize_filename(yt.title)
    filename = f"{title}.jpg"
    filepath = f"{OUTPUT_PATH}/{filename}"
    
    try:
        response = requests.get(thumbnail_url)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Download complete! File saved to: {os.path.abspath(filepath)}")
    except requests.exceptions.RequestException as e:
        print(f"Error during download: " + e)


def stream_to_string(stream: Stream) -> str:
    """Return a string containing some info about the stream"""
    parts = ['mime_type="{stream.mime_type}"']
    if stream.includes_video_track:
        parts.extend(['res="{stream.resolution}"', 'fps="{stream.fps}"', 'vcodec="{stream.video_codec}"'])
    else:
        parts.extend(['abr="{stream.abr}"', 'acodec="{stream.audio_codec}"'])
    return " ".join(parts).format(stream=stream)



# MODULE TEST AREA
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=8mLG0gDKrbs"
    # url = input("URL: ")
    
    yt = YouTube(url)
    # list_stream(yt)
    # file = yt.streams.get_audio_only(subtype="webm")
    # print(file)
    # file.download()
    
    # download_thumbnail(yt)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        os.path.abspath()





