import threading

import pytest

from src.skiplist import SkipList

NUM_THREADS = 4
NUM_ELEMENTS = 100  # Reduced for Python performance

def thread_insert_fn(skiplist, start, end):
    for i in range(start, end):
        skiplist.insert_element(i, f"thread{start // NUM_ELEMENTS}_{i}")

def test_multithreaded_inserts():
    skiplist = SkipList(6)
    threads = []
    for t in range(NUM_THREADS):
        start = t * NUM_ELEMENTS
        end = start + NUM_ELEMENTS
        th = threading.Thread(target=thread_insert_fn, args=(skiplist, start, end))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()

    assert skiplist.size() == NUM_THREADS * NUM_ELEMENTS
    # Spot check
    assert skiplist.search_element(NUM_ELEMENTS) is True