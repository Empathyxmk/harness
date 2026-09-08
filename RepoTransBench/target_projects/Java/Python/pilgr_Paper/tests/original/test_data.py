import pytest
from src.paperdb.testdata.test_data_generator import genPersonList, genPersonMap, genPerson
from src.paperdb.testdata.person import PersonArg
from collections import deque
import collections
import datetime

class DummyBook(dict):
    def write(self, key, value):
        self[key] = value
    def read(self, key, default=None):
        return self.get(key, default)
    def destroy(self):
        self.clear()

class DummyPaper:
    _store = DummyBook()
    @classmethod
    def init(cls, ctx=None):
        cls._store = DummyBook()
    @classmethod
    def book(cls):
        return cls._store

@pytest.fixture(autouse=True)
def setup():
    DummyPaper.init()
    DummyPaper.book().destroy()
    yield

def test_put_empty_list():
    inserted = genPersonList(0)
    DummyPaper.book().write("persons", inserted)
    value = DummyPaper.book().read("persons")
    assert value == []

def test_put_get_list():
    inserted = genPersonList(100)
    DummyPaper.book().write("persons", inserted)
    persons = DummyPaper.book().read("persons")
    assert persons == inserted

def test_put_map():
    inserted = genPersonMap(100)
    DummyPaper.book().write("persons", inserted)
    persons_map = DummyPaper.book().read("persons")
    assert persons_map == inserted

def test_put_pojo():
    person = genPerson(PersonArg("alex"), 1)
    DummyPaper.book().write("profile", person)
    saved_person = DummyPaper.book().read("profile")
    assert saved_person == person
    assert saved_person is not person

def test_put_sub_abstract_list_random_access():
    origin = genPersonList(100)
    sublist = origin[10:30]
    _test_read_write_without_class_check(sublist)

def test_put_sub_abstract_list():
    origin = deque(genPersonList(100))
    sublist = list(origin)[10:30]
    _test_read_write_without_class_check(sublist)

def test_put_linked_list():
    origin = deque(genPersonList(100))
    _test_read_write(origin)

def test_put_arrays_as_lists():
    _test_read_write(["123", "345"])

def test_put_collections_empty_list():
    _test_read_write([])

def test_put_collections_empty_map():
    _test_read_write({})

def test_put_collections_empty_set():
    _test_read_write(set())

def test_put_singleton_list():
    _test_read_write(["item"])

def test_put_singleton_set():
    _test_read_write({"item"})

def test_put_singleton_map():
    _test_read_write({"key": "value"})

def test_put_georgian_calendar():
    gcal = datetime.datetime.now()
    _test_read_write(gcal)

def test_put_synchronized_list():
    # Just a normal list, Python lists are thread safe in global interpreter lock
    _test_read_write(list())

def test_read_write_class_without_no_arg_constructor():
    _test_read_write(PersonArg("name"))

def _test_read_write_without_class_check(origin_obj):
    DummyPaper.book().write("obj", origin_obj)
    read_obj = DummyPaper.book().read("obj")
    assert read_obj == origin_obj
    return read_obj

def _test_read_write(origin_obj):
    read_obj = _test_read_write_without_class_check(origin_obj)
    assert type(read_obj) == type(origin_obj)