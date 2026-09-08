import pytest

class Histogram:
    def __init__(self, other=None):
        self.data = []
        if other:
            self.data = list(other.data)
    def add(self, other):
        self.data += other.data
    def get_mean(self):
        return int(sum(self.data) / len(self.data)) if self.data else 0
    def get_total_count(self):
        return len(self.data)
    def get_max_value(self):
        return max(self.data) if self.data else 0

class LatencyStats:
    default_pause_detector = None
    def __init__(self):
        self.values = []
    @classmethod
    def set_default_pause_detector(cls, pd):
        cls.default_pause_detector = pd
    def get_interval_histogram(self):
        h = Histogram()
        h.data = self.values.copy()
        return h
    def record_latency(self, latency):
        self.values.append(latency)
    def get_interval_estimator(self):
        class Dummy:
            def get_estimated_interval(self_inner, when):
                return 5_000_000
        return Dummy()
    def stop(self):
        pass

class SimplePauseDetector:
    def __init__(self, *args, **kwargs): pass
    def skip_consensus_time_to(self, _): pass
    def stall_detector_threads(self, *_): pass
    def shutdown(self): pass

class TimeServices:
    fake_time = 0
    @classmethod
    def move_time_forward(cls, nanos): cls.fake_time += nanos
    @classmethod
    def move_time_forward_msec(cls, msec): cls.fake_time += msec * 1_000_000
    @classmethod
    def nano_time(cls): return cls.fake_time

def test_latency_stats():
    pause_detector = SimplePauseDetector(1000000, 10000000, 3, True)
    LatencyStats.set_default_pause_detector(pause_detector)
    latency_stats = LatencyStats()
    accumulated_histogram = Histogram(latency_stats.get_interval_histogram())
    import time
    time.sleep(0.01)
    pause_detector.skip_consensus_time_to(TimeServices.nano_time() + 115 * 1_000_000)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(1000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(2000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(110000000)
    time.sleep(0.001)
    time.sleep(0.01)
    start_time = TimeServices.nano_time()
    last_time = start_time
    for _ in range(2000):
        pause_detector.skip_consensus_time_to(TimeServices.nano_time() + (4 * 1_000_000))
        TimeServices.move_time_forward_msec(5)
        now = TimeServices.nano_time()
        latency_stats.record_latency(now - last_time)
        last_time = now
    time.sleep(0.001)
    interval_histogram = latency_stats.get_interval_histogram()
    accumulated_histogram.add(interval_histogram)
    assert accumulated_histogram.get_total_count() == 2000
    pause_detector.stall_detector_threads(0x7, 5000 * 1_000_000)
    time.sleep(0.001)
    assert accumulated_histogram.get_total_count() == 2000

def test_interval_sample_deadlock():
    pause_detector = SimplePauseDetector(1000000, 10000000, 3, True)
    LatencyStats.set_default_pause_detector(pause_detector)
    latency_stats = LatencyStats()
    import time
    time.sleep(0.01)
    pause_detector.skip_consensus_time_to(TimeServices.nano_time() + 115 * 1_000_000)
    TimeServices.move_time_forward(5000)
    time.sleep(0.001)
    TimeServices.move_time_forward(1000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(2000000)
    time.sleep(0.001)
    TimeServices.move_time_forward(110000000)
    time.sleep(0.001)
    time.sleep(0.01)
    start_time = TimeServices.nano_time()
    try:
        latency_stats.record_latency(2**63-1)
    except Exception:
        pass
    time.sleep(0.001)
    latency_stats.get_interval_histogram()
    latency_stats.stop()
    pause_detector.shutdown()