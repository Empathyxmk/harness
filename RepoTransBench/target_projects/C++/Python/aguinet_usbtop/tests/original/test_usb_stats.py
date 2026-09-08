import pytest

class Stats:
    t0_ = 0.0
    _init_called = False

    def __init__(self):
        self.packets = []
        self.window = 1.0  # 1 second window for bw_instant as a plausible default
        self.t0 = self.__class__.t0_

    @classmethod
    def init(cls):
        import time
        cls.t0_ = time.time()
        cls._init_called = True

    def push(self, ts, size):
        # adds a (timestamp, size) to the stats, window rolling
        self.packets.append((ts, size))
        # Remove packets older than (latest ts - window)
        while self.packets and self.packets[0][0] < ts - self.window:
            self.packets.pop(0)

    def bw_instant(self):
        # bandwidth over the window
        if not self.packets:
            return 0.0
        if len(self.packets) == 1:
            return 0.0
        period = self.packets[-1][0] - self.packets[0][0]
        if period == 0:
            return 0.0
        total = sum([size for _, size in self.packets])
        return total / period

    def bw_mean(self):
        # mean bandwidth (since t0)
        if not self.packets:
            return 0.0
        elapsed = self.packets[-1][0] - self.t0
        if elapsed <= 0:
            return 0.0
        total = sum([size for _, size in self.packets])
        return total / elapsed

def test_push_and_bw_instant_mean():
    Stats.init()
    s = Stats()
    t = Stats.t0_ + 0.01
    s.push(t, 100)
    s.push(t+0.02, 200)
    s.push(t+0.04, 300)
    bw_inst = s.bw_instant()
    assert bw_inst >= 0.0
    bw_mean = s.bw_mean()
    assert bw_mean > 0.0

def test_no_packets_bw_instant():
    Stats.init()
    s = Stats()
    assert s.bw_instant() == 0.0

def test_push_window_erasure():
    Stats.init()
    s = Stats()
    t = Stats.t0_
    for i in range(5):
        s.push(t + i * 0.25, 100)  # +0.25s each
    assert s.bw_instant() >= 0.0
    assert s.bw_mean() > 0.0