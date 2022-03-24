import eyed3
from eyed3.id3 import ID3_V2_4, ID3_V1_1
from loguru import logger

def tag_mp3(mp3_file: str, artist: str, title: str, url: str):
    logger.debug('Tagging mp3. artist={}, title={}, url={}', 
                 artist, title, url)

    audiofile = eyed3.load(mp3_file)
    audiofile.tag.artist = artist
    audiofile.tag.title = title
    audiofile.tag.comments.set(f"url = {url}")

    audiofile.tag.save(version=ID3_V1_1)
    audiofile.tag.save(version=ID3_V2_4)