import pytest

class JAXBStudent:
    def __init__(self, name=None, age=None):
        self._name = name
        self._age = age

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

def test_student_public():
    student = JAXBStudent("Jordan", 30)
    assert student.get_name() == "Jordan"
    assert student.get_age() == 30