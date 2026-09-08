import pytest

class SUT:
    def hello(self):
        return "Hello"
    def talk(self):
        return "How are you?"
    def bye(self):
        return "Bye"

@pytest.fixture
def system_under_test():
    return SUT()

def test_hello(system_under_test):
    assert system_under_test.hello() == "Hello"

def test_talking(system_under_test):
    assert system_under_test.talk() == "How are you?"

def test_bye(system_under_test):
    assert system_under_test.bye() == "Bye"