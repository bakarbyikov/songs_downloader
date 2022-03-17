# -*- coding: utf-8 -*-
import concurrent.futures
from loguru import logger
import queue
import random
import threading
import time
import os
from pytube import Search, YouTube
from tqdm import tqdm
from main import download_song

SONGS_PATH = r"C:\Users\Pisun\Music\The Zone - Dublin\0"


def searcher(queue, event):
    songs = tuple(filter(lambda x: x.endswith('.mp3'),
                         os.listdir(SONGS_PATH)))
    logger.info(f"Searcher finded {len(songs)} songs")
    for song in songs:
        if event.is_set():
            break
        full_name, _, _ = song.rpartition('.')
        logger.info(f"Searcher searching for {full_name}")
        video = Search(full_name).results[0]
        logger.info(f"Searcher find video {full_name} -> {video.title}")
        url = video.watch_url
        logger.info(f"Searcher find {url}")
        queue.put(url)

    event.set()


def downloader(queue, event):
    while not event.is_set() or not queue.empty():
        url = queue.get()
        logger.info(f"Downloader downloading {url}")
        download_song(url)


if __name__ == "__main__":
    pipeline = queue.Queue(maxsize=16)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
        logger.info("Submitting searcher")
        executor.submit(searcher, pipeline, event)
        logger.info("Submitting downloaders")
        for i in range(8):
            executor.submit(downloader, pipeline, event)
        
        while True:
            try:
                pass
            except KeyboardInterrupt:
                event.set()





