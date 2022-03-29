import os
import uuid
from typing import Tuple

import youtube_dl
from loguru import logger

from trim_fork.metadata import extract_artist_title, trim_parentheses
from trim_fork.normalizer import normalize_song
from trim_fork.renamer import rename_song
from trim_fork.tagger import tag_mp3


@logger.catch
def download_song(url: str, output: str=None):
    artist, title = extract_youtube_artist_title(url)
    logger.info('Song name set to {}', f'{artist} - {title}')

    mp3_file = download_from_youtube(url)
    mp3_file = rename_song(mp3_file, artist, title, output)
    normalize_song(mp3_file)
    tag_mp3(mp3_file, artist, title, url)

    return mp3_file


@logger.catch
def download_from_youtube(url: str) -> str:
        logger.debug('Downloading from youtube url={}', url)

        uid = str(uuid.uuid4())
        filename = f'trimmer_dl_{uid}'

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{filename}.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            retcode = ydl.download([url])
            assert retcode == 0

        full_filename = f'{filename}.mp3'
        assert os.path.isfile(full_filename)
        logger.debug('Song downloaded tmpfile={}', full_filename)

        return full_filename


@logger.catch
def fetch_youtube_metadata(url: str) -> Tuple[str, str, str]:
    logger.debug('fetching metadata from youtube page: {}', url)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        einfo = ydl.extract_info(url, download=False)

        track = einfo.get('track')
        artist = einfo.get('artist') or einfo.get('creator')
        full_title = einfo.get('title') or einfo.get('alt_title')

        logger.debug('youtube page metadata fetched {}; {}; {}', 
                     artist, track, full_title)
        return artist, track, full_title


@logger.catch
def extract_youtube_artist_title(url: str) -> Tuple[str, str]:
    artist, track, full_title = fetch_youtube_metadata(url)
    if artist and track:
        return artist, trim_parentheses(track)

    return extract_artist_title(full_title)


if __name__ == "__main__":
    url = r'https://www.youtube.com/watch?v=bTS9XaoQ6mg'
    download_song(url)