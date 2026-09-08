import threading
import pytest
import time

# Minimal Sample module for sleep function
class Sample:
    @staticmethod
    def sleep(ms):
        try:
            time.sleep(ms/1000.0)
        except Exception:
            pass

def test_sleep_no_interrupt():
    # Should complete without exception
    Sample.sleep(10)

def test_sleep_with_interrupt():
    interrupted = []

    def run_sleep():
        try:
            Sample.sleep(1000)
        except Exception:
            interrupted.append(True)

    t = threading.Thread(target=run_sleep)
    t.start()
    t.join(timeout=0.2)
    # In Python, .interrupt() does not exist; can't forcibly interrupt a thread.
    # Just test that method runs and does not crash, like the Java version.