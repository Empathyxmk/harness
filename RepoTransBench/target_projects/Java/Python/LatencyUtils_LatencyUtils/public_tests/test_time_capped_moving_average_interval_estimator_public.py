import time

class PauseDetector:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify_listeners(self, length, when):
        for listener in self.listeners:
            listener.handle_pause_event(length, when)

class MyArtificialPauseDetectorPublic(PauseDetector):
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

    def record_interval(self, timestamp):
        self.times.append(timestamp)
        if len(self.times) > self.window_count + 1:
            self.times.pop(0)

    def get_estimated_interval(self, now):
        if len(self.times) < 2:
            return 0
        oldest_time = self.times[0]
        newest_time = self.times[-1]
        times_in_window = self.times[-(self.window_count + 1):]
        intervals = [times_in_window[i] - times_in_window[i - 1] for i in range(1, len(times_in_window))]
        if now > newest_time + self.cap_ns:
            return 2**63 - 1
        avg = int(sum(intervals) / len(intervals)) if intervals else 0
        return avg

def test_window_behavior_public():
    pause_detector = MyArtificialPauseDetectorPublic()
    estimator = TimeCappedMovingAverageIntervalEstimator(16, 500_000_000, pause_detector)
    time.sleep(0.01)

    now = 0

    for _ in range(5000):
        now += 15
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 15

    for _ in range(8):
        now += 30
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 22

    for _ in range(4):
        now += 60
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 32

    pause_detector.record_pause(600_000_000, now + 600_000_000)
    now += 600_000_000
    time.sleep(0.01)
    assert estimator.get_estimated_interval(now) == 32

    for _ in range(4):
        estimator.record_interval(now)
        now += 60
    assert estimator.get_estimated_interval(now) == 47

    now = 1_600_000_000
    assert estimator.get_estimated_interval(now) == 2**63 - 1

    estimator.record_interval(now)
    for _ in range(8):
        now += 10
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 10

    pause_detector.record_pause(700_000_000, 2_001_000_000)
    now = 2_001_000_000
    time.sleep(0.01)
    estimator.record_interval(now)

    for _ in range(8):
        now += 15
        estimator.record_interval(now)

    now = 2_001_000_000 + (10 * 1_000_000)
    assert estimator.get_estimated_interval(now) == 1_000_000

    now = 2_700_000_000
    assert estimator.get_estimated_interval(now) == 2**63 - 1