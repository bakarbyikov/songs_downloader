# -*- coding: utf-8 -*-
from cmath import pi
import concurrent.futures
from loguru import logger
import queue
import random
import threading
import time
import os
from pytube import Search, YouTube
from tqdm import tqdm
from main import down_song_by_name
from songs_list import get_songs


@logger.catch
def downloader(queue, event, number, pbar):
    logger.debug(f"Downloader {number} started")
    
    while not event.is_set() and not queue.empty():
        song = queue.get()
        logger.debug(f"Now {queue.qsize()} songs in queue")
        # logger.debug("Processing song {}", song)
        try:
            down_song_by_name(song)
        except Exception:
            pass
        finally:
            pbar.update(1)

    logger.debug("Downloader {} exiting normally", number)


@logger.catch
def main():
    thread_count = 32

    # logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.remove()
    logger.add("log_info.txt", level="DEBUG")

    event = threading.Event()
    pipeline = queue.Queue()
    for song in get_songs():
        pipeline.put(song)
    last_count = pipeline.qsize()
    
    with tqdm(total=last_count) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
            logger.debug("Submitting downloaders")

            for i in range(thread_count):
                executor.submit(downloader, pipeline, event, i, pbar)

            # try:
            #     while True:
            #         pass
            #         # count = pipeline.qsize()
            #         # if last_count != count:
            #         #     pbar.update(last_count - count)
            #         #     last_count = count
                        
            # except KeyboardInterrupt:
            #     event.set()


if __name__ == "__main__":
    main()
