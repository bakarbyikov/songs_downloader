# -*- coding: utf-8 -*-
import os
from pytube import Search, YouTube
# from moviepy.editor import AudioFileClip
from trimmer.trim_source import trim_url
from trimmer.downloader import extract_youtube_artist_title

SONGS_PATH = r"C:\Users\Pisun\Music\The Zone - Dublin\0"
SAVE_PATH = r"C:\Users\Pisun\Documents\condapoj\song_browse\songs"


def download_song(url: str, output: str,
                  full_name: str, no_fade: bool = True):

    artist, _, title = extract_youtube_artist_title(url)
    if not artist or not title:
        artist, _, title = full_name.partition(' - ')
    new_file_name = f'{artist} - {title}.mp3'
    new_file_path = os.path.join(output, new_file_name)

    trim_url(url, artist, title, False, no_fade, False,
             None, None, None, new_file_path)


if __name__ == '__main__':
    songs = filter(lambda x: x.endswith('.mp3'),
                   os.listdir(SONGS_PATH))

    for song in songs:
        full_name, _, _ = song.rpartition('.')
        video = Search(full_name).results[0]
        url = video.watch_url
        download_song(url, SAVE_PATH, full_name)
