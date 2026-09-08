import pytest

class Application:
    pass  # Dummy application class to simulate Application in Android

class ApplicationTest:
    def __init__(self):
        # Normally would pass Application class to super constructor; simulated in Python
        self.application_class = Application

def test_application_created():
    # Equivalent to the Java ApplicationTest constructor and basic instantiation check
    app_test = ApplicationTest()
    assert app_test.application_class == Application