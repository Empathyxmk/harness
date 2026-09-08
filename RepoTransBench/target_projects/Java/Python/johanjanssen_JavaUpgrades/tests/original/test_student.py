import pytest

class Student:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_info():
        return "Java class"

    def is_blank_name(self):
        if self.name is None:
            return True
        return not self.name.strip()

def test_constructor_and_get_info():
    student = Student("Alice")
    assert Student.get_info() == "Java class"
    assert student is not None

def test_is_blank_name_null():
    student = Student(None)
    assert student.is_blank_name()

def test_is_blank_name_empty_string():
    student = Student("")
    assert student.is_blank_name()

def test_is_blank_name_space_only():
    student = Student("   ")
    assert student.is_blank_name()

def test_is_blank_name_non_blank():
    student = Student("Bob")
    assert not student.is_blank_name()