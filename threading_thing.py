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
from main import get_songs_list, search_by_filename, SAVE_PATH
from trim_fork.my_downloader import download_song


@logger.catch
def downloader(queue, event, number):
    logger.debug("Downloader started")
    
    while not event.is_set() or not queue.empty():
        song = queue.get()
        logger.debug("Processing song {}", song)
        url = search_by_filename(song)
        logger.debug("Downloading {}", url)
        download_song(url, SAVE_PATH)

    logger.debug("Downloader {} exiting normally", number)
    if not event.is_set():
        event.set()


@logger.catch
def main():
    thread_count = 32

    logger.add("log_info.txt", level="DEBUG")

    event = threading.Event()
    pipeline = queue.Queue()
    for song in get_songs_list():
        pipeline.put(song)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        logger.debug("Submitting downloaders")

        for i in range(thread_count):
            executor.submit(downloader, pipeline, event, i)


if __name__ == "__main__":
    main()
