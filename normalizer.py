import os
from typing import Optional

from loguru import logger
from pydub import AudioSegment


def normalize_song(mp3_file: str):
    logger.debug('Normalizing song: {}', mp3_file)
    song = AudioSegment.from_mp3(mp3_file)

    normalize_volume(song)
    trim(song)
        
    duartion = len(song)
    logger.debug('Saving song. duration={}', duration_to_human(duartion))
    song.export(mp3_file, format="mp3")


def trim(song):
    logger.debug('Trimming silence')
    start_trim = detect_leading_silence(song)
    end_trim = detect_leading_silence(song.reverse(), margin=0)
    logger.debug('Silence detected start_trim={}, end_trim={}', start_trim, end_trim)
    pre_duration = len(song)
    song = song[start_trim:-end_trim]
    post_duration = len(song)
    logger.debug('Silence trimmed. pre_duration={}, post_duration={}', duration_to_human(pre_duration), duration_to_human(post_duration))


def normalize_volume(song):
    volume = calculate_volume(song)
    logger.debug('Normalizing volume level. Volume={volume:.2f}dB', volume=volume)
    gain = -volume
    song = song.apply_gain(gain)
    logger.debug('Volume normalized. gain={gain:.2f}', gain=gain)


def calculate_volume(song: AudioSegment) -> float:
    volume = song.max_dBFS
    return volume
    # if volume < -0.1:
    #     return volume

    # lower_vol = 10
    # tmp_clip = '.anti_clip.mp3'
    # logger.debug('Detecting clipping')
    # lowered = song.apply_gain(-lower_vol)
    # lowered.export(tmp_clip, format="mp3")
    # lowered = AudioSegment.from_mp3(tmp_clip)
    # os.remove(tmp_clip)
    # return lowered.max_dBFS + lower_vol


def detect_leading_silence(song: AudioSegment, margin: int = 100) -> int:
    silence_threshold = -45.0  # dB
    trim_ms = 0  # ms
    chunk_size = 50  # ms

    while (song[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold
           and trim_ms < len(song)):
        trim_ms += chunk_size

    if trim_ms >= margin:
        return trim_ms - margin
    return trim_ms


def duration_to_human(ms: int) -> str:
    sec = ms / 1000
    if sec < 60:
        return f'{sec:.3f}s'
    minutes = int(sec // 60)
    sec = sec % 60
    return f'{minutes}:{sec:06.3f}'
