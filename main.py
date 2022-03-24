# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
from typing import List
from loguru import logger
from pytube import Search, YouTube
# from trimmer.trim_source import trim_url
# from trimmer.downloader import extract_youtube_artist_title
from my_downloader import download_song

# SAVE_PATH = r"C:\Users\Pisun\Documents\condapoj\song_browse\songs"
SAVE_PATH = r"./songs"

def is_song_file(name: str):
    return name.endswith('.mp3')


def save_songs_list(songs: List):
    with open("Songs_list.txt", 'w') as f:
        for s in songs[:-1]:
            f.write(s)
            f.write('\n')
        f.write(songs[-1])


def list_songs():
    path = input("Enter songs directory: ")
    files = os.listdir(path)
    songs = filter(is_song_file, files)
    return list(songs)


def get_songs_list():
    try:
        with open("Songs_list.txt", 'r') as f:
            songs = f.readlines()
    except FileNotFoundError:
        songs = list_songs()
        save_songs_list(songs)
    else:
        songs = list(map(str.strip, songs))
    return songs


def correct_name(name: str) -> str:
    blocked_sumbols = r'<>:"/\|?*'
    for s in blocked_sumbols:
        if s in name:
            name = name.replace(s, '-')
    return name


# def create_artist_title_path(url: str):
#     artist, track = extract_youtube_artist_title(url)
#     artist, track = artist or "undefined", track or "undefined"
#     full_name = f'{artist} - {track}.mp3'
#     full_name = correct_name(full_name)
#     path = os.path.join(SAVE_PATH, full_name)
#     return artist, track, path


# def download_song(url: str, no_fade: bool = True):
#     artist, track, path = create_artist_title_path(url)

#     trim_url(url, artist, track, False, no_fade, False,
#              None, None, None, path)


def search_songs():
    songs = get_songs_list()

    urls_to_download = list()
    for song in tqdm(songs, desc="Extracting names"):
        full_name, _, _ = song.rpartition('.')
        video = Search(full_name).results[0]
        url = video.watch_url
        urls_to_download.append(url)

    return urls_to_download


def main():
    for url in tqdm(search_songs(), desc="Downloading songs"):
        download_song(url)


if __name__ == '__main__':
    main()