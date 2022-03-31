import os
from typing import List
from settings import SONG_LIST_PATH, SONGS_FOLDER

def is_mp3_file(name: str) -> bool:
    return name.endswith('.mp3')


def save_songs_list(songs: List[str]):
    with open(SONG_LIST_PATH, 'w') as f:
        for s in songs[:-1]:
            f.write(s)
            f.write('\n')
        f.write(songs[-1])


def open_song_list(path: str) -> List[str]:
    with open(SONG_LIST_PATH, 'r') as f:
        songs = [s.strip() for s in f.readlines()]
    return songs


def list_songs(path: str) -> List[str]:
    files = os.listdir(path)
    songs = filter(is_mp3_file, files)
    songs = [s[:-4] for s in songs]
    return list(songs)


def get_songs() -> List[str]:
    try:
        songs = open_song_list(SONG_LIST_PATH)
    except FileNotFoundError:
        songs = list_songs(SONGS_FOLDER)
        save_songs_list(songs)
    return songs