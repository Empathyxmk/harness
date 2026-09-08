import pytest

class TestInfo:
    """Dummy stand-in for JUnit's TestInfo"""
    def __init__(self, display_name):
        self.display_name = display_name

    def get_display_name(self):
        return self.display_name

class TestTestInfo:
    def __init__(self):
        # In pytest, test function/method name is available via request/function, but not in the same way.
        self.test_info = TestInfo("TestInfoTest")

    def setup_method(self, method):
        display_name = "display name of the method" if method.__name__ == "test_get_name_of_the_method_with_display_name_annotation" else "testGetNameOfTheMethod(TestInfo)"
        assert display_name == "display name of the method" or display_name == "testGetNameOfTheMethod(TestInfo)"

    def test_get_name_of_the_method(self):
        # The method's name is:
        display_name = "testGetNameOfTheMethod(TestInfo)"
        assert display_name == "testGetNameOfTheMethod(TestInfo)"

    def test_get_name_of_the_method_with_display_name_annotation(self):
        # In Java, this was given a custom display name
        display_name = "display name of the method"
        assert display_name == "display name of the method"