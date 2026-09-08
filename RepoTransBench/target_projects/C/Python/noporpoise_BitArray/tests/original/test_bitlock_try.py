import threading
import time
import pytest

NWORKERS = 10
LIMIT = 10000

class Bitlock:
    """
    Simulate a bitlock using a bytearray and bitfield access.
    """
    def __init__(self, num_bits):
        # Using one byte per 8 bits
        self.locks = bytearray((num_bits + 7)//8)
        self.lock = threading.Lock()

    def try_acquire(self, pos):
        byte_idx = pos // 8
        bit_idx = pos % 8
        mask = 1 << bit_idx
        with self.lock:
            if not (self.locks[byte_idx] & mask):
                self.locks[byte_idx] |= mask
                return True
            return False

    def all_set(self):
        # Check if all bits up to LIMIT are set
        for i in range((LIMIT+7)//8):
            if self.locks[i] != 0xff:
                return False
        return True

def cumm_sum(num):
    return num * ((num+1)//2) + (0 if num & 1 else num//2)

class TestThread(threading.Thread):
    def __init__(self, lockarr, thread_id):
        super().__init__()
        self.id = thread_id
        self.result = 0
        self.locks = lockarr

    def run(self):
        for i in range(LIMIT):
            got = self.locks.try_acquire(i)
            if got:
                self.result += i
            if (i & 0xff) == 0xff:
                time.sleep(0.00005)
                time.sleep(0)  # mimic sched_yield()

def test_bitlock_try_threading():
    locks = Bitlock(LIMIT)
    workers = [TestThread(locks, i) for i in range(NWORKERS)]

    for w in workers:
        w.start()
    for w in workers:
        w.join()

    sum_ = sum(w.result for w in workers)
    expsum = cumm_sum(LIMIT-1)
    pass_cond = (sum_ == expsum)

    assert pass_cond, f"sum mismatch: got {sum_}, expected {expsum}"

    # All bits must be set
    assert locks.all_set(), f"locks not all ones!"