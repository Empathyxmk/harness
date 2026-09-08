def test_moving_average_interval_estimator_public():
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
            avg = int(sum(intervals) / len(intervals))
            return avg

    estimator = MovingAverageIntervalEstimator(512)
    now = 0
    for _ in range(8000):
        now += 25
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(now) == 25

    for _ in range(400):
        now += 50
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(0) == 37

    for _ in range(200):
        now += 80
        estimator.record_interval(now)
    assert estimator.get_estimated_interval(0) == 53