import pytest

class JAXBStudent:
    def __init__(self, id_=None, name=None):
        self._id = id_
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_id(self, id_):
        self._id = id_

    def set_name(self, name):
        self._name = name

    def __str__(self):
        return f"JAXBStudent(id={self._id}, name={self._name})"

def test_all_args_constructor_and_accessors():
    student = JAXBStudent(2, "Jane Doe")
    assert student.get_id() == 2
    assert student.get_name() == "Jane Doe"
    student.set_id(3)
    student.set_name("John Smith")
    assert student.get_id() == 3
    assert student.get_name() == "John Smith"

def test_to_string_not_null():
    student = JAXBStudent(42, "Test User")
    s = str(student)
    assert s is not None
    assert "42" in s
    assert "Test User" in s