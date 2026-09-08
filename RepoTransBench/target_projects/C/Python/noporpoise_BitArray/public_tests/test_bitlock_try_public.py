import threading
import time

NWORKERS = 7
LIMIT = 5279

class Bitlock:
    def __init__(self, num_bits):
        self.locks = bytearray((num_bits + 7)//8)
        self.lock = threading.Lock()
        self.num_bits = num_bits

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
            if (i & 0x7f) == 0x7f:
                time.sleep(0.00005)
                time.sleep(0)

def test_bitlock_try_public():
    locks = Bitlock(LIMIT)
    workers = [TestThread(locks, i) for i in range(NWORKERS)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()

    sum_ = sum(w.result for w in workers)
    expsum = cumm_sum(LIMIT-1)
    assert sum_ == expsum, f"PUBLIC TEST sum mismatch: got {sum_}, expected {expsum}"
    assert locks.all_set(), f"locks not all ones!"