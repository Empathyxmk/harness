import pytest

class Application:
    pass  # Dummy application class

class ApplicationPublicTest:
    def __init__(self):
        self.application_class = Application

def test_application_public_created():
    # Same as ApplicationPublicTest instantiation
    app_test = ApplicationPublicTest()
    assert app_test.application_class == Application