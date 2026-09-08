import pytest

class Person:
    def __init__(self, ssn, firstname, lastname):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname

def test_returns_none_for_non_existing_student():
    db = type("CustomDB", (), {
        "find": lambda self, ssn: None
    })()
    assert db.find('123-45-6789') is None

def test_store_and_retrieve_new_person_custom_db():
    class CustomDB:
        def __init__(self):
            self.students = {'111-22-3333': Person('111-22-3333', 'Alan', 'Turing')}
        def find(self, ssn):
            return self.students.get(ssn)
    db = CustomDB()
    p = db.find('111-22-3333')
    assert isinstance(p, Person)
    assert p.ssn == '111-22-3333'
    assert p.firstname == 'Alan'
    assert p.lastname == 'Turing'