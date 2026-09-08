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

class TestSleepPublic:
    def test_calls_usleep_with_correct_value_public(self, sleep):
        sleep._usleepCalled = None
        sleep.sleep(5)
        assert sleep._usleepCalled == 5000000

    def test_throws_on_negative_seconds_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep(-10)

    def test_throws_on_decimal_seconds_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep(2.7)

    def test_throws_on_string_input_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep("baz")

class TestMsleepPublic:
    def test_calls_usleep_with_correct_value_public(self, sleep):
        sleep._usleepCalled = None
        sleep.msleep(111)
        assert sleep._usleepCalled == 111000

    def test_throws_on_negative_ms_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep(-50)

    def test_throws_on_decimal_ms_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep(3.3)

    def test_throws_on_string_input_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep("qux")