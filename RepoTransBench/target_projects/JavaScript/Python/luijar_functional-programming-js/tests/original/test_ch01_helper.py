import pytest

# Dummy Person and db for test
class Person:
    def __init__(self, ssn, firstname, lastname):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname

class HelperDB:
    def find(self, ssn):
        mapping = {
            '444-44-4444': Person('444-44-4444', 'Alonzo', 'Church'),
            '444444444': Person('444-44-4444', 'Alonzo', 'Church')
        }
        return mapping.get(ssn, None)

@pytest.fixture
def helper_db():
    return HelperDB()

def test_db_has_find_method(helper_db):
    assert helper_db is not None
    assert hasattr(helper_db, "find") and callable(helper_db.find)

def test_find_existing_ssn_returns_person(helper_db):
    person = helper_db.find('444-44-4444')
    assert isinstance(person, Person)
    assert person.ssn == '444-44-4444'
    assert person.firstname == 'Alonzo'
    assert person.lastname == 'Church'

def test_alternate_ssn_lookup_returns_correct_person(helper_db):
    person = helper_db.find('444444444')
    assert isinstance(person, Person)
    assert person.ssn == '444-44-4444'

def test_find_unknown_ssn_returns_none(helper_db):
    person = helper_db.find('not-a-ssn')
    assert person is None