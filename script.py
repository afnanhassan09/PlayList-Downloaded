#Paste your playlist link at line 42

from pytube import Playlist, YouTube
import os
from moviepy.editor import AudioFileClip


def clean_filename(filename):
    forbidden_chars = '<>:"/\\|?*'
    for char in forbidden_chars:
        filename = filename.replace(char, '')
    return filename

def download_audio_as_mp3(playlist_url, download_path="Song Downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        
    pl = Playlist(playlist_url)
    for audio_url in pl.video_urls:
        try:
            audio = YouTube(audio_url)
            stream = audio.streams.filter(only_audio=True).order_by('abr').desc().first()
            cleaned_title = clean_filename(audio.title)
            audio_file_path = stream.download(output_path=download_path, filename=f"{cleaned_title}.mp4")
        
            # Convert the downloaded file to mp3 using moviepy
            mp3_file_path = os.path.splitext(audio_file_path)[0] + '.mp3'
            with AudioFileClip(audio_file_path) as audio_clip:
                audio_clip.write_audiofile(mp3_file_path, codec='mp3')
        
            # Optionally remove the original mp4 file
            os.remove(audio_file_path)
        
            print(f"Downloaded and converted: {audio.title} to {os.path.abspath(mp3_file_path)}\n")
        except Exception as e:
            print(f"Error downloading {audio.title}: {e}")

    print("All songs successfully downloaded")



# Paste your playlist link here
playlist_url = ""
download_audio_as_mp3(playlist_url=playlist_url)
