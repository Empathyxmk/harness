import pytest

class MockSleep:
    def __init__(self):
        self._usleepCalled = None

    def usleep(self, v):
        self._usleepCalled = v

    def sleep(self, seconds):
        if not isinstance(seconds, (int, float)):
            raise Exception('Expected number of seconds')
        if seconds < 0 or seconds % 1 != 0:
            raise Exception('Expected number of seconds')
        self.usleep(seconds * 1000000)

    def msleep(self, milis):
        if not isinstance(milis, (int, float)):
            raise Exception('Expected number of miliseconds')
        if milis < 0 or milis % 1 != 0:
            raise Exception('Expected number of miliseconds')
        self.usleep(milis * 1000)

@pytest.fixture(autouse=True)
def sleep():
    s = MockSleep()
    yield s

class TestSleepPublicDifferentInput:
    def test_calls_usleep_correctly_for_positive_input_public(self, sleep):
        sleep._usleepCalled = None
        sleep.sleep(4)
        assert sleep._usleepCalled == 4000000

    def test_throws_for_negative_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep(-7)

    def test_throws_for_decimal_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of seconds"):
            sleep.sleep(6.3)

class TestMsleepPublicDifferentInput:
    def test_calls_usleep_correctly_public(self, sleep):
        sleep._usleepCalled = None
        sleep.msleep(45)
        assert sleep._usleepCalled == 45000

    def test_throws_for_negative_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep(-15)

    def test_throws_for_decimal_public(self, sleep):
        with pytest.raises(Exception, match="Expected number of miliseconds"):
            sleep.msleep(0.2)

class TestUsleepPublicDifferentInputs:
    def test_calls_usleep_with_exact_microseconds_public(self, sleep):
        sleep._usleepCalled = None
        sleep.usleep(3600)
        assert sleep._usleepCalled == 3600

    def test_throws_for_negative_public(self, sleep):
        sleep.usleep(-2222)
        assert sleep._usleepCalled == -2222