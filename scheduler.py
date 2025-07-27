import random
import signal
import time

from dataclasses import dataclass
from itertools import batched
from math import ceil
from multiprocessing.pool import Pool
from scrapping import *
from typing import Sequence


def split_into_batches(
        sequence: Sequence[str],
        no_batches: int,
        chunk_size: int
    ) -> list[list[tuple[str]]]:
    chunks = list(batched(sequence, chunk_size))
    batch_size = ceil(len(chunks) / no_batches) 
    return list(batched(chunks, batch_size))


def process_chunk(chunk: Sequence[str]) -> list[dict[str, str | None]]:
    """ Wraps batch search, keeping a common WebDriver object for the same search

        Args:
           chunk: The chunk/batch of keys to be searched

        Returns:
            scrapped_data: list of dicts following the structure: 
            {'doc-number': <search_key>, 'data': <html_string>}
    """
    driver, wait = setup_driver()
    navigate_to_search_page(driver, wait)
    results = []
    
    try:
        for result in batch_search(driver, wait, chunk):
            results.append(result)
    
    finally:
        driver.quit()
        return results


def mock_process_chunk(chunk: Sequence[str]) -> list[dict[str, str | None]]:
    """ Simulates the behaviour of the`process_chunk`function
        without sending any requests
        
        Args:
           chunk: The chunk/batch of keys to be searched

        Returns:
            dummy_data: list of dicts following the structure: 
            {'doc-number': <search_key>, 'data': <search_key>}
    """
    results = []
    try:
        time.sleep(random.randint(1, 5))
        for search_key in chunk:
            results.append({'doc-number': search_key, 'data': search_key})
    finally:
        print("\tclosing driver")
        return results


class Credentials:
    pass


class Storage:
    pass


@dataclass
class SchedulerConfig:
    chunk_size: int
    no_workers: int
    blob_max_size: int


class Scheduler:
    pass


class ShutdownRequestedException(Exception):

    def __init__(self, signal):
        super().__init__()
        self.signal = signal


if __name__ == '__main__':
    
    mock_keys = [f'{i:06d}' for i in range(1, 101)]
    mock_keys_batched = list(batched(mock_keys, 5))
    pool = Pool(2)
    results = []
    try:
        for elem in pool.imap_unordered(mock_process_chunk, mock_keys_batched):
            print(elem)
            results.append(elem)
    except KeyboardInterrupt:
        pool.terminate()
        print('KEYBOARD INTERRUPT')
    finally:
        print(len(results))
    