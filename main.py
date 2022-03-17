# -*- coding: utf-8 -*-
import os
from tqdm import tqdm
from pytube import Search, YouTube
from trimmer.trim_source import trim_url
from trimmer.downloader import extract_youtube_artist_title

SONGS_PATH = r"C:\Users\Pisun\Music\The Zone - Dublin"
SAVE_PATH = r"C:\Users\Pisun\Documents\condapoj\song_browse\songs"


def correct_name(name: str) -> str:
    blocked_sumbols = r'<>:"/\|?*'
    for s in blocked_sumbols:
        if s in name:
            name = name.replace(s, '-')
    return name


def create_artist_title_path(url: str):
    artist, track = extract_youtube_artist_title(url)
    artist, track = artist or "undefined", track or "undefined"
    full_name = f'{artist} - {track}.mp3'
    full_name = correct_name(full_name)
    path = os.path.join(SAVE_PATH, full_name)
    return artist, track, path


def download_song(url: str, no_fade: bool = True):
    artist, track, path = create_artist_title_path(url)

    trim_url(url, artist, track, False, no_fade, False,
             None, None, None, path)


def search_songs():
    songs = tuple(filter(lambda x: x.endswith('.mp3'),
                        os.listdir(SONGS_PATH)))

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
    try:
        main()
    except Exception as e:
        error = e
        print("\a")
        raise e
