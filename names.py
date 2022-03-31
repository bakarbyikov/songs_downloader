from pytube import YouTube
from typing import Tuple
from re import sub


def is_mp3_file(name: str) -> bool:
    return name.endswith('.mp3')


def delete_extention(name: str) -> str:
    return name[:-4]


def get_from_meta(video: YouTube) -> Tuple[str, str]:
    author, title = None, None
    for meta in video.metadata:
        if "Artist" in meta:
            author = meta["Artist"]
        if "Song" in meta:
            title = meta["Song"]
        if author and title:
            break
    return author, title


def get_from_title(video: YouTube) -> Tuple[str, str]:
    yt_title = video.title
    if " - " in yt_title:
        author, _, title = yt_title.partition(' - ')
    else:
        author, title = None, yt_title
    return author, title


def get_from_video(video: YouTube) -> Tuple[str, str]:
    author, title = video.author, video.title
    return author, title


def get_song_name_and_artist(video: YouTube) -> Tuple[str, str]:
    author, title = get_from_title(video)
    if author is None or title is None:
        author, title = get_from_meta(video)
    if author is None or title is None:
        author, title = get_from_video(video)

    author, title = correct_name(author), correct_name(title)
    
    return author, title


def correct_name(name: str) -> str:
    if is_mp3_file(name):
        name = delete_extention(name)
    name = delete_parentheses(name)

    blocked_sumbols = r'<>:"/\|?*' + r"'"
    for s in blocked_sumbols:
        if s in name:
            name = name.replace(s, '-')
    return name.strip()


def generate_fullname(artist: str, name: str) -> str:
    return correct_name(f"{artist} - {name}")


def song_name_from_video(video: YouTube) -> str:
    artist, name = get_song_name_and_artist(video)
    fullname = generate_fullname(artist, name)
    return fullname


def delete_parentheses(name: str) -> str:
    return sub("[([{].+[])}]", '', name)