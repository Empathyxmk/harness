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

def test_put_empty_list_public():
    inserted = genPersonList(3)
    DummyPaper.book().write("persons_pub", inserted)
    assert len(DummyPaper.book().read("persons_pub")) == 3
    DummyPaper.book().write("persons_pub", [])
    assert DummyPaper.book().read("persons_pub") == []

def test_put_get_list_public():
    inserted = genPersonList(7)
    DummyPaper.book().write("alt_persons", inserted)
    persons = DummyPaper.book().read("alt_persons")
    assert persons == inserted

def test_put_map_public():
    inserted = genPersonMap(5)
    DummyPaper.book().write("alt_persons_map", inserted)
    persons_map = DummyPaper.book().read("alt_persons_map")
    assert persons_map == inserted

def test_put_pojo_public():
    person = genPerson(PersonArg("test"), 42)
    DummyPaper.book().write("new_profile", person)
    saved_person = DummyPaper.book().read("new_profile")
    assert saved_person == person
    assert saved_person is not person

def test_put_sub_abstract_list_random_access_public():
    origin = genPersonList(20)
    sublist = origin[5:17]
    _test_read_write_without_class_check(sublist)

def test_put_sub_abstract_list_public():
    origin = deque(genPersonList(20))
    sublist = list(origin)[5:17]
    _test_read_write_without_class_check(sublist)

def test_put_linked_list_public():
    origin = deque(genPersonList(15))
    _test_read_write(origin)

def test_put_arrays_as_lists_public():
    _test_read_write(["abc", "xyz", "def"])

def test_put_collections_empty_list_public():
    _test_read_write([])

def test_put_collections_empty_map_public():
    _test_read_write({})

def test_put_collections_empty_set_public():
    _test_read_write(set())

def test_put_singleton_list_public():
    _test_read_write(["singleton_item"])

def test_put_singleton_set_public():
    _test_read_write({"singleton"})

def test_put_singleton_map_public():
    _test_read_write({"onlykey": "onlyvalue"})

def test_put_georgian_calendar_public():
    gcal = datetime.datetime(1999, 8, 13)
    _test_read_write(gcal)

def test_put_synchronized_list_public():
    arr = ["hello"]
    _test_read_write(arr)

def test_read_write_class_without_no_arg_constructor_public():
    _test_read_write(PersonArg("alice"))

def _test_read_write_without_class_check(origin_obj):
    DummyPaper.book().write("obj_pub", origin_obj)
    read_obj = DummyPaper.book().read("obj_pub")
    assert read_obj == origin_obj
    return read_obj

def _test_read_write(origin_obj):
    read_obj = _test_read_write_without_class_check(origin_obj)
    assert type(read_obj) == type(origin_obj)