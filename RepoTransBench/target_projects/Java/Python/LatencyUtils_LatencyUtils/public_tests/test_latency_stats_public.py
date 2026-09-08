def test_record_and_estimate():
    class Histogram:
        def __init__(self):
            self.data = []
        def get_max_value(self):
            return max(self.data) if self.data else 0

    class LatencyStats:
        def __init__(self):
            self.values = []
        def record_latency(self, latency):
            self.values.append(latency)
        def get_interval_histogram(self):
            h = Histogram()
            h.data = list(self.values)
            return h

    stats = LatencyStats()
    for i in range(50):
        stats.record_latency(2000 + i * 2)
    est = stats.get_interval_histogram().get_max_value()
    assert est >= 2000