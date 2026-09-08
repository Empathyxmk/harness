from ratelimit.utils import now
import time

def test_public_now_monotonicity():
    # now() should be non-decreasing between closely spaced calls
    t1 = now()
    time.sleep(0.01)
    t2 = now()
    assert t2 >= t1

def test_public_now_close_to_time_time():
    # now() and time.time() should be very close within ~1 second
    t1 = now()
    t2 = time.time()
    assert abs(t2 - t1) < 1