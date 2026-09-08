import pytest

class SUT:
    def __init__(self, name):
        self.system_name = name
        self._verified = False

    def get_system_name(self):
        return self.system_name

    def is_verified(self):
        return self._verified

    def verify(self):
        self._verified = True

def test_system_not_verified():
    system_under_test = SUT("Our system under test")
    assert system_under_test.get_system_name() == "Our system under test"
    assert not system_under_test.is_verified()

def test_system_under_verification():
    system_under_test = SUT("Our system under test")
    system_under_test.verify()
    assert system_under_test.get_system_name() == "Our system under test"
    assert system_under_test.is_verified()