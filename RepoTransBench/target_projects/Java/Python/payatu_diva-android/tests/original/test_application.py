import pytest

class Application:
    def __init__(self):
        pass

class ApplicationTest:
    def __init__(self):
        self.app = Application()

def test_application_init():
    app_test = ApplicationTest()
    assert isinstance(app_test.app, Application)