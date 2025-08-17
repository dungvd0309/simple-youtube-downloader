from pytubefix import YouTube, Stream, Caption, StreamQuery
import os 
import subprocess

OUTPUT_PATH = "output/"

def sanitize_filename(name: str):
    illegal = '\\/:*?"<>|'
    trans = str.maketrans('', '', illegal)
    name = name.translate(trans)
    return name

def download_video(yt: YouTube):
    """Download the best video and audio stream and merge them with ffmpeg."""
    ys = yt.streams
    video = ys.get_highest_resolution(progressive=False)
    audio = ys.get_audio_only()

    video_path = video.download(filename="video_only.mp4")
    audio_path = audio.download(filename="audio_only.m4a")

    title = sanitize_filename(yt.title)
    output_path = f"{title}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c", "copy",
        "-movflags", "+faststart",
        output_path
    ]
    subprocess.run(cmd, check=True)

    os.remove(video_path)
    os.remove(audio_path)

def download_caption(yt: YouTube):
    """Download a.en caption."""
    cap: Caption = yt.captions.get('a.en')
    with open(f"a-en.srt", "w", encoding="utf-8") as f:
        f.write(cap.generate_srt_captions())

def list_stream(yt: YouTube):
    """List all DASH stream of an YouTube object."""
    ys = yt.streams.filter(is_dash=True)

    for index, item in enumerate(ys):
        item: Stream
        parts = ['mime_type="{item.mime_type}"']
        if item.includes_video_track:
            parts.extend(['res="{item.resolution}"', 'fps="{item.fps}"', 'vcodec="{item.video_codec}"'])
        else:
            item.abr
            parts.extend(['abr="{item.abr}"', 'acodec="{item.audio_codec}"'])
        print(f'{index}.', " ".join(parts).format(item=item))

def list_caption(yt: YouTube):
    """List all captions of an YouTube object."""
    for index, item in enumerate(yt.caption_tracks):
        print(f"{index}. {item.name} - {item.code}")


url = "https://www.youtube.com/watch?v=8mLG0gDKrbs"

yt = YouTube(url)
list_stream(yt)






