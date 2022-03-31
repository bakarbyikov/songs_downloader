# -*- coding: utf-8 -*-
import concurrent.futures
from loguru import logger
import queue
import threading
from tqdm import tqdm

from main import down_song_by_name
from songs_list import get_songs


@logger.catch
def downloader(queue, event, number, pbar):
    logger.debug(f"Downloader {number} started")
    
    while not event.is_set() and not queue.empty():
        song = queue.get()
        logger.debug(f"Now {queue.qsize()} songs in queue")
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
    
    with tqdm(total=pipeline.qsize()) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
            logger.debug("Submitting downloaders")

            for i in range(thread_count):
                executor.submit(downloader, pipeline, event, i, pbar)


if __name__ == "__main__":
    main()
