# Additional unit tests for src/sleep_module.py

import pytest

class MockSleep:
    def __init__(self):
        self._usleepCalled = None

    def usleep(self, value):
        self._usleepCalled = value

    def sleep(self, seconds):
        if not isinstance(seconds, (int, float)):
            raise Exception('Expected number of seconds')
        if seconds < 0 or seconds % 1 != 0:
            raise Exception('Expected number of seconds')
        self.usleep(seconds * 1000000)

    def msleep(self, miliseconds):
        if not isinstance(miliseconds, (int, float)):
            raise Exception('Expected number of miliseconds')
        if miliseconds < 0 or miliseconds % 1 != 0:
            raise Exception('Expected number of miliseconds')
        self.usleep(miliseconds * 1000)


@pytest.fixture(scope="function")
def sleep():
    return MockSleep()

class TestSleep:
    def test_calls_usleep_with_correct_value(self, sleep):
        sleep._usleepCalled = None
        sleep.sleep(3)
        assert sleep._usleepCalled == 3000000

    def test_throws_on_negative_seconds(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep(-2)

    def test_throws_on_decimal_seconds(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep(1.5)

    def test_throws_on_string_input(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep("foo")

class TestMsleep:
    def test_calls_usleep_with_correct_value(self, sleep):
        sleep._usleepCalled = None
        sleep.msleep(250)
        assert sleep._usleepCalled == 250000

    def test_throws_on_negative_ms(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep(-10)

    def test_throws_on_decimal_ms(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep(1.7)

    def test_throws_on_string_input(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep("bar")