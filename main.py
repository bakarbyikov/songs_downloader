# -*- coding: utf-8 -*-
from os import path
import re
from typing import List, Tuple
from loguru import logger
from pytube import Search, YouTube
from pydub import AudioSegment, silence, effects
from tqdm import tqdm

from songs_list import get_songs
from names import generate_fullname, get_song_name_and_artist, song_name_from_video
from settings import SAVE_PATH


def find_best_match(full_name: str, videos: List[YouTube]) -> YouTube:
    return videos[0]


def search_song(full_name: str) -> YouTube:
    if full_name.endswith(".mp3"):
        full_name = full_name[:-4]
    
    results = Search(full_name).results
    assert len(results) > 0, f"Video '{full_name}' not found"
    video = find_best_match(full_name, results)
    return video


def download_audio(video: YouTube) -> str:
    stream = video.streams.get_audio_only()
    path = stream.download(output_path="./tmp", skip_existing=False, max_retries=10)
    logger.info(f"Audio downloaded  to '{path}'")
    return path


def trim(song: AudioSegment) -> AudioSegment:
    args = silence_thresh, chunk_size = -50, 10

    start_trim = silence.detect_leading_silence(song, *args)
    end_trim = silence.detect_leading_silence(song.reverse(), *args)
    assert start_trim < len(song), "Song is all silent"

    trimmed = song[start_trim:-end_trim]
    logger.info(f"Song trimed from {len(song)} to {len(trimmed)}")
    return trimmed


def process_song(song_path: str, name: str, artist:str, url:str) -> str:
    song = AudioSegment.from_file(song_path)
    song = trim(song)
    song = effects.normalize(song)
    logger.info("Song nomalized")
    new_name = generate_fullname(name, artist)
    new_path = path.join(SAVE_PATH, new_name) + ".mp3"
    comment = f"downloaded from {url}"
    tags = {"comment": comment, "artist": artist, "title": name}
    song.export(new_path, format='mp3', tags=tags)
    logger.info(f"Song saved succsesfully to '{new_path}'")
    return new_path


def down_song(video: YouTube) -> str:
    path = download_audio(video)
    name, artist = get_song_name_and_artist(video)
    url = video.watch_url
    path = process_song(path, name, artist, url)
    return path


@logger.catch
def down_song_by_name(song:str) -> str:
    video = search_song(song)
    logger.info(f"Searched for song '{song}' -> '{video.title}'({video.watch_url})")
    return down_song(video)


@logger.catch
def down_song_by_url(url:str) -> str:
    video = YouTube(url)
    return down_song(video)


@logger.catch
def main():
    songs = get_songs()

    with open("songs_search_3.txt", "w") as f:
        for song in tqdm(songs, desc="Searching songs"):
            video = search_song(song)
            fullname = song_name_from_video(video)
            f.write(f"'{song}' -> '{fullname}'({video.watch_url})\n")
            # logger.info(f"Searched for song '{song}' -> '{fullname}'({video.watch_url})")


if __name__ == '__main__':
    main()
