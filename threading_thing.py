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
from main import download_song, get_songs_list

@logger.catch
def searcher(queue, event):
    logger.debug("Searcher started")
    songs = get_songs_list()
    logger.debug("Searcher finded {} songs", len(songs))
    for song in songs:
        if event.is_set():
            logger.debug("Searcher exiting because event set")
            return
        full_name, _, _ = song.rpartition('.')
        logger.debug("Searcher searching for {}", full_name)
        video = Search(full_name).results[0]
        logger.info("Searcher find video {} -> {}", full_name, video.title)
        url = video.watch_url
        logger.debug("Searcher find url: {}", url)
        queue.put(url)

    logger.debug("Searcher exiting normally")


@logger.catch
def downloader(queue, event):
    logger.debug("Downloader started")
    while not event.is_set() or not queue.empty():
        url = queue.get()
        logger.debug("Downloader downloading {}", url)
        download_song(url)
    logger.debug("Downloader exiting normally")


if __name__ == "__main__":
    logger.add("log_info.txt", level="INFO")
    pipeline = queue.Queue(maxsize=64)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
        logger.debug("Submitting searcher")
        executor.submit(searcher, pipeline, event)
        logger.debug("Submitting downloaders")
        for i in range(8):
            executor.submit(downloader, pipeline, event)
        
        while True:
            try:
                pass
            except KeyboardInterrupt:
                logger.debug("Event set by main")
                event.set()
                break





