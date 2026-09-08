import pytest

class SUT:
    def __init__(self, name):
        self.name = name

    def can_receive_regular_work(self):
        return True

    def can_receive_additional_work(self):
        return False

@pytest.mark.skip(reason="Feature is still under construction.")
class TestDisabledClass:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.system_under_test = SUT("Our system under test")

    def test_regular_work(self):
        assert self.system_under_test.can_receive_regular_work()

    def test_additional_work(self):
        assert not self.system_under_test.can_receive_additional_work()