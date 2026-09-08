import pytest

class NoJobException(Exception):
    pass

class SUT:
    def __init__(self, name):
        self.name = name
        self.jobs = []

    def run(self, value=None):
        if value is None:
            raise NoJobException()
        elif value == 1000:
            raise NoJobException("No jobs on the execution list!")
        else:
            self.jobs.append(value)

def test_expected_exception():
    system_under_test = SUT("Our system under test")
    with pytest.raises(NoJobException):
        system_under_test.run()

def test_catch_exception():
    system_under_test = SUT("Our system under test")
    with pytest.raises(NoJobException) as excinfo:
        system_under_test.run(1000)
    assert str(excinfo.value) == "No jobs on the execution list!"