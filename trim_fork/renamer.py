import os
from pathlib import Path
from loguru import logger


def rename_song(mp3_file: str, artist: str, title: str, output: str=None) -> str:
    dirname, filename = os.path.split(mp3_file)
    if artist.strip():
        new_filename = f'{artist.strip()} - {title.strip()}.mp3'
    else:
        new_filename = f'{title.strip()}.mp3'
    new_path = Path(output or dirname) / new_filename
    os.rename(mp3_file, new_path)
    logger.debug('Song renamed. new_name={}', new_path)
    return new_path