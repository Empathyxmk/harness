import pytest

# Mocking Student class as per the original test logic
class Student:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_info():
        return "Java record"

    def is_blank_name(self):
        if self.name is None:
            return True
        return not self.name.strip()


def test_get_info():
    assert Student.get_info() == "Java record"

def test_is_blank_name_blank():
    s = Student("   ")
    assert s.is_blank_name()

def test_is_blank_name_non_blank():
    s = Student("Eve")
    assert not s.is_blank_name()