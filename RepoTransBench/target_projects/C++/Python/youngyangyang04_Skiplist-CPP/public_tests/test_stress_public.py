import threading
import pytest

from src.skiplist import SkipList

THREAD_COUNT_PUBLIC = 3
NUM_PER_THREAD_PUBLIC = 100  # Reduced for Python performance

def insert_range_public(skiplist, start, count, tid):
    for i in range(count):
        key = start + i
        skiplist.insert_element(key, f"pubt{tid}_{key}")

def test_multithreaded_public():
    skiplist = SkipList(8)
    threads = []
    for t in range(THREAD_COUNT_PUBLIC):
        th = threading.Thread(target=insert_range_public, args=(skiplist, t * 500, NUM_PER_THREAD_PUBLIC, t))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()

    total_inserted = THREAD_COUNT_PUBLIC * NUM_PER_THREAD_PUBLIC
    assert skiplist.size() == total_inserted

    # Check some known keys
    assert skiplist.search_element(0) is True
    assert skiplist.search_element(500) is True
    assert skiplist.search_element(1000) is True
    assert skiplist.search_element(123456) is False  # Not inserted

    # Delete a range in one thread, check size and search
    for i in range(20, 70):
        skiplist.delete_element(i)
    assert skiplist.search_element(20) is False
    assert skiplist.size() == total_inserted - 50

    for i in range(10):
        assert skiplist.search_element(0 + i) is True
        assert skiplist.search_element(1000 + i) is True

    # Print to indicate public stress test passed (for parity with C++ test)
    print("[Public Stress Test Passed]")