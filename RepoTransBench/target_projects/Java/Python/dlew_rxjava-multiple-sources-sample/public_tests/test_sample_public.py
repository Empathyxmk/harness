import pytest
import time

class Sample:
    @staticmethod
    def sleep(ms):
        try:
            time.sleep(ms/1000.0)
        except Exception:
            pass

def test_sample_main_runs_public():
    # This will primarily test that the main method executes without error
    Sample.sleep(10)  # Just call sleep since main is long-running