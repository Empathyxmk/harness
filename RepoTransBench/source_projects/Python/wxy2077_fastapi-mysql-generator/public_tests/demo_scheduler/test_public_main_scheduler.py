import pytest

def test_public_schedule_addition():
    # Different input/test data compared to private
    from datetime import datetime, timedelta
    start = datetime(2025, 7, 1, 10, 0)
    delta = timedelta(seconds=20)
    # Custom simple function: scheduling next time
    def next_time(start, delta, count):
        times = []
        t = start
        for _ in range(count):
            t += delta
            times.append(t)
        return times

    times = next_time(start, delta, 2)
    assert len(times) == 2
    assert times[0] > start
    assert (times[1] - times[0]).total_seconds() == 20

def test_public_schedule_times_unique():
    from datetime import datetime, timedelta
    # Use different delta/inputs for public test
    start = datetime(2024, 12, 31, 23, 45)
    delta = timedelta(minutes=3)
    times = [start + i*delta for i in range(4)]
    assert len(set(times)) == 4
    assert times[-1] > start