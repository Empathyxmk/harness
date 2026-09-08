import pytest

class JAXBStudent:
    def __init__(self, name=None, age=None):
        self._name = name
        self._age = age

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

class JAXBService:
    def create_xml(self, student):
        if student is None:
            return ""
        return f"<student><name>{student.get_name()}</name><age>{student.get_age()}</age></student>"

def test_create_student_xml_public():
    jaxb_service = JAXBService()
    student = JAXBStudent("Charlie Public", 25)
    xml = jaxb_service.create_xml(student)
    assert "Charlie Public" in xml
    assert "25" in xml