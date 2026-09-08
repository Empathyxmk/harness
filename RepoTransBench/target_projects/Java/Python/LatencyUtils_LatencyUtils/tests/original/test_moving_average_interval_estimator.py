import pytest

class MovingAverageIntervalEstimator:
    def __init__(self, window_size):
        self.window_size = window_size
        self.intervals = []

    def record_interval(self, timestamp):
        if not self.intervals:
            self.intervals.append(timestamp)
        else:
            self.intervals.append(timestamp)
            if len(self.intervals) > self.window_size + 1:
                self.intervals.pop(0)

    def get_estimated_interval(self, _timestamp):
        if len(self.intervals) < 2:
            return 0
        intervals = [self.intervals[i] - self.intervals[i - 1] for i in range(1, len(self.intervals))]
        if not intervals:
            return 0
        # Match Java's integer division (truncation towards 0)
        avg = int(sum(intervals) / len(intervals))
        return avg

def test_moving_average_interval_estimator():
    estimator = MovingAverageIntervalEstimator(1024)
    now = 0
    for _ in range(10000):
        now += 20
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 20

    for _ in range(512):
        now += 40
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(0) == 30

    for _ in range(256):
        now += 60
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(0) == 40