import pytest
import time
import subprocess

# Py translation of: public_tests/sleep_api.public.test.js

def assert_approx_equal(val1, val2, epsilon=150):
    diff = val1 - val2
    if diff > epsilon:
        pytest.fail(f'wait was too long: {diff} > {epsilon}')
    elif diff < -epsilon:
        pytest.fail(f'wait was too long: {diff} < {-epsilon}')

try:
    from src import sleep_module as sleep
except ImportError:
    sleep = None

@pytest.mark.skipif(sleep is None, reason="sleep_module not available")
class TestPublicIntegrationSleepAPI:
    def test_sleep_works_for_new_input(self):
        sleep_time = 2
        start = time.time()
        sleep.sleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time * 1000)

    def test_sleep_works_for_one_public(self):
        sleep_time = 1
        start = time.time()
        sleep.sleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time * 1000)

    def test_sleep_does_not_allow_negative_numbers_public(self):
        with pytest.raises(ValueError):
            sleep.sleep(-8)

    def test_works_with_child_process_public(self):
        sleep_time = 2
        subprocess.Popen(["echo", "hello"])
        start = time.time()
        sleep.sleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time * 1000)

    def test_usleep_works_typical_microseconds_public(self):
        sleep_time = 100000
        start = time.time()
        sleep.usleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time / 1000)

    def test_usleep_works_large_microseconds_public(self):
        sleep_time = 1500000
        start = time.time()
        sleep.usleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time / 1000)

    def test_usleep_does_not_allow_negative_public(self):
        with pytest.raises(ValueError):
            sleep.usleep(-111)

    def test_msleep_works_new_normal_input_public(self):
        sleep_time = 6
        start = time.time()
        sleep.msleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time)

    def test_msleep_does_not_allow_negative_public(self):
        with pytest.raises(ValueError):
            sleep.msleep(-13)

    def test_msleep_does_not_allow_decimal_public(self):
        with pytest.raises(ValueError):
            sleep.msleep(5.7)