from menu_template import OptionMenu, MenuItem, TextPromptMenu, ResultMenu, clear_console, press_to_continue
import sys
import msvcrt
from tqdm import tqdm
import pytubefix.exceptions as yt_exceptions
from pytubefix import YouTube, Stream
import urllib.error
from youtube_handler import *


PROGRAM_TITLE = "Simple YouTube Downloader"


# Test function
def func(num = None):
    clear_console()
    if num is None:
        print("A function has been run")
    else:
        print(f"Function {num} has been run")
    input()

# ==========================
#       MENU CLASSES
# ==========================
# TODO-1: Show file size in menu selection
# TODO : Remove args= in menu, use lambda function instead(still haven't remove arg)
# TODO: Add more video info

class VideoSelectionMenu(OptionMenu):

    def __init__(self, yt: YouTube, selection_only = False):
        self.yt = yt
        self.selection_only = selection_only
        self.selected_stream: Stream = None
        super().__init__("Select video stream: ")

    def initialize_item_list(self):
        streams = get_video_stream_list(self.yt)
        
        # Add the best option
        best = streams.get_highest_resolution(progressive=False)

        if self.selection_only:
            action_best = lambda s=best: self.set_selected_stream(s)
            self.add_menu_item(
                MenuItem("1", f"(Auto) {stream_to_string(best)}", action=action_best, isExitOption=True)
            )
        else:
            action_best = lambda s=best: (
                clear_console(),
                download_video_only(self.yt, s),
                press_to_continue()
            )
            self.add_menu_item(
                MenuItem("1", f"(Auto) {stream_to_string(best)}", action=action_best)
            )

        # Add the other options
        for index, stream in enumerate(streams):
            if self.selection_only:
                action = lambda s=stream: self.set_selected_stream(s)
                self.add_menu_item(
                    MenuItem(f"{index+2}", stream_to_string(stream), action=action, isExitOption=True)
                )
            else:
                action = lambda s=stream: (
                    clear_console(),
                    download_video_only(self.yt, s),
                    press_to_continue()
                )
                self.add_menu_item(
                    MenuItem(f"{index+2}", stream_to_string(stream), action=action)
                )

        self.add_menu_item(MenuItem("b", "Back", isExitOption=True))

    def set_selected_stream(self, selected_stream: Stream):
        self.selected_stream = selected_stream

    def get_selected_stream(self):
        return self.selected_stream

    

class AudioSelectionMenu(OptionMenu):

    def __init__(self, yt: YouTube, selection_only = False):
        self.yt = yt
        self.selection_only = selection_only
        self.selected_stream: Stream = None
        super().__init__("Select audio stream: ")

    def initialize_item_list(self):
        streams = get_audio_stream_list(self.yt)

        # Add the best option
        best = streams.get_audio_only()

        if self.selection_only:
            action_best = lambda s=best: self.set_selected_stream(s)
            self.add_menu_item(
                MenuItem("1", f"(Auto) {stream_to_string(best)}", action=action_best, isExitOption=True)
            )
        else:
            action_best = lambda s=best: (
                clear_console(),
                download_audio_only(self.yt, s),
                press_to_continue()
            )
            self.add_menu_item(
                MenuItem("1", f"(Auto) {stream_to_string(best)}", action=action_best)
            )

        # Add the other options
        for index, stream in enumerate(streams):
            if self.selection_only:
                action = lambda s=stream: self.set_selected_stream(s)
                self.add_menu_item(
                    MenuItem(f"{index+2}", stream_to_string(stream), action=action, isExitOption=True)
                )
            else:
                action = lambda s=stream: (
                    clear_console(),
                    download_audio_only(self.yt, s),
                    press_to_continue()
                )
                self.add_menu_item(
                    MenuItem(f"{index+2}", stream_to_string(stream), action=action)
                )

        self.add_menu_item(MenuItem("b", "Back", isExitOption=True))

    def set_selected_stream(self, selected_stream: Stream):
        self.selected_stream = selected_stream

    def get_selected_stream(self):
        return self.selected_stream

class CaptionSelectionMenu(OptionMenu):

    def __init__(self, yt: YouTube):
        self.yt = yt
        super().__init__("Select caption: ")

    def initialize_item_list(self):
        captions = get_caption_list(self.yt)

        for index, caption in enumerate(captions):
            caption: Caption
            action = lambda c=caption: (
                clear_console(),
                download_caption(self.yt, c.code),
                press_to_continue()
            )
            self.add_menu_item(MenuItem(index+1, f'{caption.name}: {caption.code}', action=action))

        self.add_menu_item(MenuItem("b", "Back", isExitOption=True))


class DownloadMenu(OptionMenu):

    def __init__(self, title: str, url: str):
        self.url = url
        self.pbar = None
        self.yt = YouTube(url=url, 
                          on_progress_callback=self.progress_callback, 
                          on_complete_callback=self.complete_callback)
        super().__init__(title)
    
    def display_menu(self):
        print(f"URL: {self.url}")
        print(f"Title: {self.yt.title}")
        super().display_menu()

    def initialize_item_list(self):
        self.add_menu_item(MenuItem("1", "Video with audio", action=self.download_video_with_audio))
        self.add_menu_item(MenuItem("2", "Video only", menu=VideoSelectionMenu(self.yt)))
        self.add_menu_item(MenuItem("3", "Audio only", menu=AudioSelectionMenu(self.yt)))
        self.add_menu_item(MenuItem("4", "Caption", menu=CaptionSelectionMenu(self.yt)))
        self.add_menu_item(MenuItem("5", "Thumbnail", lambda:func(5)))
        self.add_menu_item(MenuItem("b", "Back", isExitOption=True))
        self.add_menu_item(MenuItem("q", "Quit", quit))

    def progress_callback(self, stream: Stream, chuck: bytes, bytes_remaining: int):
        """Handle download bar."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        if self.pbar is None:
            print(f"Selected stream: {stream_to_string(stream)}")
            self.pbar = tqdm(total=total_size, desc="Downloading", unit="B", unit_scale=True)
        
        self.pbar.n = bytes_downloaded
        self.pbar.refresh()

    def complete_callback(self, stream: Stream, file_path):
        """Handle download complete event."""
        if self.pbar:
            self.pbar.close()
        self.pbar = None

        print(f"Download completed. File saved to: {file_path}")

    def download_video_with_audio(self):
        """Handle video menu, audio menu, and merging video and audio stream."""
        clear_console()
        # Choose video stream
        video_sel_menu = VideoSelectionMenu(self.yt, selection_only=True)
        video_sel_menu.execute_menu()
        video = video_sel_menu.get_selected_stream()
        if video is None:
            return

        # Choose audio stream
        audio_sel_menu = AudioSelectionMenu(self.yt, selection_only=True)
        audio_sel_menu.execute_menu()
        audio = audio_sel_menu.get_selected_stream()
        if audio is None:
            return

        download_video(self.yt, video, audio)
        press_to_continue()


    
class UrlMenu(TextPromptMenu):
    pass

if __name__ == "__main__": 
    while True:
        # url_menu = UrlMenu("YouTube URL:")
        # url = url_menu.execute_menu()

        url = "https://www.youtube.com/watch?v=8mLG0gDKrbs"

        if url:
            if url.lower() in ["q", "quit", "exit"]:
                break
            try:
                download_menu = DownloadMenu("Download options", url)
                download_menu.execute_menu()
            except yt_exceptions.RegexMatchError:
                ResultMenu("Invalid YouTube URL.").execute_menu()
            except yt_exceptions.VideoUnavailable:
                ResultMenu("Invalid YouTube URL.").execute_menu()
            except urllib.error.URLError:
                ResultMenu("Could not get URL. Please check your internet connection.").execute_menu()
        