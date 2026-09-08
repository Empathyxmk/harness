import pytest
import threading
from src.rlog import RingLogSingleton, LOG_INIT, LOG_ERROR

def get_current_millis():
    import time
    return int(time.time() * 1000)

def thread_job(start, end):
    for i in range(start, end):
        LOG_ERROR("my number is number my number is my number is my number is my number is my number is my number is %d", i)

def test_multithreaded_logging():
    RingLogSingleton.instance().clear()
    LOG_INIT("log", "myname", 3)
    start_ts = get_current_millis()

    N_THREAD = 5
    N_LOOP = 2000  # Reduced from 1e7 for test runtime
    threads = []
    for n in range(N_THREAD):
        t = threading.Thread(target=thread_job, args=(n*N_LOOP, (n+1)*N_LOOP))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end_ts = get_current_millis()

    # There should be N_THREAD*N_LOOP ERROR log entries.
    entries = [e for e in RingLogSingleton.instance().entries if e.startswith("[ERROR]")]
    assert len(entries) == N_THREAD*N_LOOP
    # Print run duration for info, but we just check functional logging.
    print(f"time use {end_ts-start_ts}ms")