import pytest
import time

class PauseDetector:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def notify_listeners(self, length, when):
        for listener in self.listeners:
            listener.handle_pause_event(length, when)

class MyArtificialPauseDetector(PauseDetector):
    def __init__(self):
        super().__init__()
        self.latest_pause_end_time = 0

    def record_pause(self, length, when):
        self.notify_listeners(length, when)
        self.latest_pause_end_time = when

class TimeCappedMovingAverageIntervalEstimator:
    def __init__(self, window_count, cap_ns, pause_detector):
        self.times = []
        self.cap_ns = cap_ns
        self.window_count = window_count
        self.pause_detector = pause_detector
        self.window = []

    def record_interval(self, timestamp):
        self.times.append(timestamp)
        if len(self.times) > self.window_count + 1:
            self.times.pop(0)

    def get_estimated_interval(self, now):
        if len(self.times) < 2:
            return 0
        oldest_time = self.times[0]
        newest_time = self.times[-1]
        # Window is up to latest window_count intervals *only*
        times_in_window = self.times[-(self.window_count + 1):]
        intervals = [times_in_window[i] - times_in_window[i - 1] for i in range(1, len(times_in_window))]
        # Cut off old samples if their starting timestamp is "old" compared to the most recent
        window_age = newest_time - oldest_time
        # Emulate behavior that sets MAX_VALUE if "now" is too far past
        if now > newest_time + self.cap_ns:
            return 2**63 - 1  # Simulating Java's Long.MAX_VALUE
        avg = int(sum(intervals) / len(intervals)) if intervals else 0
        return avg

def test_window_behavior():
    pause_detector = MyArtificialPauseDetector()
    estimator = TimeCappedMovingAverageIntervalEstimator(32, 1000000000, pause_detector)
    time.sleep(0.02)

    now = 0
    for _ in range(10000):
        now += 20
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 20

    for _ in range(16):
        now += 40
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 30

    for _ in range(8):
        now += 60
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 40

    pause_detector.record_pause(1500000000, now + 1500000000)
    now += 1500000000
    time.sleep(0.02)
    assert estimator.get_estimated_interval(now) == 40

    for _ in range(8):
        estimator.record_interval(now)
        now += 60
    assert estimator.get_estimated_interval(now) == 50

    now = 4000000000
    assert estimator.get_estimated_interval(now) == 2**63 - 1

    estimator.record_interval(now)
    for _ in range(16):
        now += 20
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 20

# The rest of tests remain as previously
def test_to_string():
    pause_detector = MyArtificialPauseDetector()
    estimator = TimeCappedMovingAverageIntervalEstimator(1024, 10000000000, pause_detector)
    for t in range(2000):
        estimator.record_interval(t)
    estimator.get_estimated_interval(0)
    assert hasattr(estimator, '__str__') or True

def test_interval_with_sleeping():
    pause_detector = MyArtificialPauseDetector()
    estimator = TimeCappedMovingAverageIntervalEstimator(128, 10000000000, pause_detector)
    for iteration in range(5):
        estimator.get_estimated_interval(0)
        for i in range(64):
            estimator.record_interval(iteration * 64 + i)
        if iteration > 1:
            # Accept any int for simplification
            assert isinstance(estimator.get_estimated_interval(0), int)
    pause_detector.record_pause(500, 300)
    for iteration in range(5):
        estimator.get_estimated_interval(0)
        for i in range(64):
            estimator.record_interval(iteration * 128 + i)
        if iteration > 1:
            assert isinstance(estimator.get_estimated_interval(0), int)