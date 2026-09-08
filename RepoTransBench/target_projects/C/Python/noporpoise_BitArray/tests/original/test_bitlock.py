import threading
import time
import pytest

NUM_LOOPS = 10000

class SharedState:
    """
    Simulate lock bits, data storage, and named mutexes.
    """
    def __init__(self, num_loops):
        self.locks = bytearray((num_loops + 7)//8)
        self.data = [0]*num_loops
        self.mutexes = [threading.Lock() for _ in range(num_loops)]

    def lock_bit(self, i):
        byte_idx = i // 8
        bit_idx = i % 8
        mask = 1 << bit_idx
        return byte_idx, mask

    def bit_set(self, i):
        byte_idx, mask = self.lock_bit(i)
        return bool(self.locks[byte_idx] & mask)

    def acquire_bitlock(self, i):
        # Spin acquire
        while True:
            acquired = self.try_acquire_bitlock(i)
            if acquired:
                return
            time.sleep(0)

    def try_acquire_bitlock(self, i):
        byte_idx, mask = self.lock_bit(i)
        with threading.Lock():
            if not (self.locks[byte_idx] & mask):
                self.locks[byte_idx] |= mask
                return True
        return False

    def release_bitlock(self, i):
        byte_idx, mask = self.lock_bit(i)
        with threading.Lock():
            if self.locks[byte_idx] & mask:
                self.locks[byte_idx] &= ~mask

    def yield_acquire_bitlock(self, i):
        # Like spin, but just yield
        while True:
            acquired = self.try_acquire_bitlock(i)
            if acquired:
                return
            time.sleep(0)

    def all_bits_zero(self):
        for v in self.locks:
            if v != 0:
                return False
        return True

def cumm_sum(num):
    return num * ((num+1)//2) + (0 if num & 1 else num//2)

class TestThread(threading.Thread):
    def __init__(self, func, state, thread_id):
        super().__init__()
        self.result = 0
        self.id = thread_id
        self.state = state
        self.func = func

    def run(self):
        self.result = self.func(self.state, self.id)

def worker_bitlock(state, thread_id):
    result = 0
    for i in range(NUM_LOOPS):
        state.yield_acquire_bitlock(i)
        result += i + state.data[i]
        state.data[i] = thread_id
        time.sleep(0.000005)
        state.release_bitlock(i)
        time.sleep(0.000005)
    return result

def worker_bitlock_spin(state, thread_id):
    result = 0
    for i in range(NUM_LOOPS):
        state.acquire_bitlock(i)
        result += i + state.data[i]
        state.data[i] = thread_id
        time.sleep(0.000005)
        state.release_bitlock(i)
        time.sleep(0.000005)
    return result

def worker_mutex(state, thread_id):
    result = 0
    for i in range(NUM_LOOPS):
        with state.mutexes[0]:
            result += i + state.data[i]
            state.data[i] = thread_id
            time.sleep(0.000005)
        time.sleep(0.000005)
    return result

def worker_mutexes(state, thread_id):
    result = 0
    for i in range(NUM_LOOPS):
        with state.mutexes[i]:
            result += i + state.data[i]
            state.data[i] = thread_id
            time.sleep(0.000005)
        time.sleep(0.000005)
    return result

import sys

@pytest.mark.parametrize("mode,worker_func", [
    ("bits", worker_bitlock),
    ("mutex", worker_mutex),
    ("mutexes", worker_mutexes),
    ("spin", worker_bitlock_spin),
])
def test_bitlock_modes(mode, worker_func):
    num_threads = 30
    state = SharedState(NUM_LOOPS)
    # init mutexes done in SharedState
    threads = [TestThread(worker_func, state, i+1) for i in range(num_threads)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    sum_ = sum(state.data) + sum(t.result for t in threads)
    expsum = cumm_sum(NUM_LOOPS-1)*num_threads + cumm_sum(num_threads)*NUM_LOOPS

    assert sum_ == expsum, f"sum {sum_} does not match expected {expsum}"

    assert state.all_bits_zero(), "locks not zeroed!"