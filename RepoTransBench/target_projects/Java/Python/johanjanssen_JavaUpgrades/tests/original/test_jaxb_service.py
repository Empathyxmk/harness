import pytest

class JAXBStudent:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = name

    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

class JAXBService:
    def marshal(self, student):
        if student is None:
            return None
        return f"<student><id>{student.get_id()}</id><name>{student.get_name()}</name></student>"

    def unmarshal(self, xml):
        if xml is None:
            return None
        # fake deserialization based on above XML
        id_start = xml.find("<id>")
        id_end = xml.find("</id>")
        name_start = xml.find("<name>")
        name_end = xml.find("</name>")
        if id_start == -1 or id_end == -1 or name_start == -1 or name_end == -1:
            return None
        id_val = int(xml[id_start+4:id_end])
        name_val = xml[name_start+6:name_end]
        return JAXBStudent(id_val, name_val)

def test_marshal_and_unmarshal():
    student = JAXBStudent()
    student.set_id(1)
    student.set_name("Test Student")
    service = JAXBService()
    xml = service.marshal(student)
    assert xml is not None
    unmarshalled = service.unmarshal(xml)
    assert unmarshalled is not None
    assert student.get_id() == unmarshalled.get_id()
    assert student.get_name() == unmarshalled.get_name()

def test_marshal_null():
    service = JAXBService()
    xml = service.marshal(None)
    assert xml is None

def test_unmarshal_null():
    service = JAXBService()
    student = service.unmarshal(None)
    assert student is None