import pytest

class ResourceForAllTests:
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.opened = True

    def close(self):
        self.opened = False

class SUT:
    def __init__(self, system_name):
        self.system_name = system_name
        self.closed = False

    def close(self):
        self.closed = True

    def can_receive_regular_work(self):
        # Simulate an SUT that can receive regular work
        return True

    def can_receive_additional_work(self):
        # Simulate an SUT that cannot receive additional work
        return False

@pytest.fixture(scope="module")
def resource_for_all_tests():
    res = ResourceForAllTests("Our resource for all tests")
    yield res
    res.close()

@pytest.fixture
def system_under_test():
    sut = SUT("Our system under test")
    yield sut
    sut.close()

def test_regular_work(resource_for_all_tests, system_under_test):
    assert system_under_test.can_receive_regular_work()

def test_additional_work(resource_for_all_tests, system_under_test):
    assert not system_under_test.can_receive_additional_work()