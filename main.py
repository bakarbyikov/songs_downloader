# -*- coding: utf-8 -*-
import os
from pytube import YouTube
from moviepy.editor import AudioFileClip

SAVE_PATH = r"C:\Users\Pisun\Documents\condapoj\song_browse\songs"


def download_video(link, output_path):
    yt = YouTube(link)
    return yt.streams.get_audio_only() \
        .download(output_path=output_path)


def mp4_to_mp3(mp4, mp3):
    with AudioFileClip(mp4) as file:
        file.write_audiofile(mp3)


def trim_song(song, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0
    assert chunk_size > 0


if __name__ == '__main__':
    # os.system('cmd /c "color a"')

    # videos_path = os.path.join(SAVE_PATH, "videos")

    # link = "https://www.youtube.com/watch?v=Yem_iEHiyJ0"
    # video = download_video(link, videos_path)
    # song_name = os.path.basename(video).replace("mp4", "mp3")
    # mp4_to_mp3(video, os.path.join(SAVE_PATH, song_name))

    path = r"C:\Users\Pisun\Documents\condapoj\song_browse\songs\videos\Frankie Goes To Hollywood - Relax (Official Video).mp4"
    with AudioFileClip(path) as song:
        trim_song(song)
        song.write_audiofile("lol.mp3")
