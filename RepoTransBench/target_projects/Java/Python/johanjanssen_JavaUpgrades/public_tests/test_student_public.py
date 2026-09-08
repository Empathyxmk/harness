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

def test_constructor_and_get_info_public():
    student = Student("Charlie")
    assert Student.get_info() == "Java class"
    assert student is not None

def test_is_blank_name_null_public():
    student = Student(None)
    assert student.is_blank_name()

def test_is_blank_name_empty_string_public():
    student = Student("\t")
    assert student.is_blank_name()

def test_is_blank_name_space_only_public():
    student = Student("    ")
    assert student.is_blank_name()

def test_is_blank_name_non_blank_public():
    student = Student("Dana")
    assert not student.is_blank_name()