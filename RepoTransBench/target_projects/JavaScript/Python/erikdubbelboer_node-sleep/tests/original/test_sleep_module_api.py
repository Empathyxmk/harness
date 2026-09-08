import pytest
import time
import subprocess
from src import sleep_module

def assert_approx_equal(val1, val2, epsilon=100):
    diff = val1 - val2
    if diff > epsilon:
        pytest.fail(f'wait was too long: {diff} > {epsilon}')
    elif diff < -epsilon:
        pytest.fail(f'wait was too long: {diff} < {-epsilon}')

class TestSleepModule:
    def test_sleep_works_for_normal_input(self):
        sleep_time = 1
        start = time.time()
        sleep_module.sleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time * 1000) # ms

    def test_sleep_works_for_zero(self):
        sleep_time = 0
        start = time.time()
        sleep_module.sleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time * 1000)

    def test_sleep_does_not_allow_negative_numbers(self):
        with pytest.raises(ValueError):
            sleep_module.sleep(-1)

    def test_sleep_works_with_child_process(self):
        sleep_time = 1
        # Start a child process (doesn't actually sleep in child)
        subprocess.Popen(['echo', 'hi'])
        start = time.time()
        sleep_module.sleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time * 1000)

class TestUsleep:
    def test_usleep_works_for_smaller_than_second(self):
        sleep_time = 250 # us
        start = time.time()
        sleep_module.usleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time / 1000)

    def test_usleep_works_for_zero(self):
        sleep_time = 0
        start = time.time()
        sleep_module.usleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time / 1000)

    def test_usleep_works_for_larger_than_second(self):
        sleep_time = 3000000
        start = time.time()
        sleep_module.usleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time / 1000)

    def test_usleep_does_not_allow_negative_numbers(self):
        with pytest.raises(ValueError):
            sleep_module.usleep(-100)

class TestMsleep:
    def test_msleep_works_for_normal_input(self):
        sleep_time = 1
        start = time.time()
        sleep_module.msleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time)

    def test_msleep_works_for_zero(self):
        sleep_time = 0
        start = time.time()
        sleep_module.msleep(sleep_time)
        end = time.time()
        assert_approx_equal((end - start)*1000, sleep_time)

    def test_msleep_does_not_allow_negative_numbers(self):
        with pytest.raises(ValueError):
            sleep_module.msleep(-100)

    def test_msleep_does_not_allow_decimal_numbers(self):
        with pytest.raises(ValueError):
            sleep_module.msleep(1.5)

class TestError:
    def test_should_throw_a_valid_error(self):
        with pytest.raises(ValueError) as e:
            sleep_module.msleep(float('inf'))
        assert str(e.value) == 'Expected number of miliseconds'