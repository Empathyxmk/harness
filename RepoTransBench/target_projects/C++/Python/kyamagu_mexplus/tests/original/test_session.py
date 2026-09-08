import pytest

class Session:
    _storage = {}
    _counter = 0

    @classmethod
    def create(cls, obj):
        cls._counter += 1
        oid = cls._counter
        cls._storage[oid] = obj
        return oid

    @classmethod
    def get(cls, oid):
        if oid not in cls._storage:
            raise KeyError("Session::get returned a NULL pointer.")
        return cls._storage[oid]

    @classmethod
    def exist(cls, oid):
        return oid in cls._storage

    @classmethod
    def destroy(cls, oid):
        if oid not in cls._storage:
            raise KeyError("Session::get returned a NULL pointer.")
        del cls._storage[oid]

    @classmethod
    def clear(cls):
        cls._storage = {}

class HypotheticalClass: pass

def test_session_create_get_exist_destroy_clear():
    id_ = Session.create(HypotheticalClass())
    assert Session.get(id_) is not None
    with pytest.raises(KeyError):
        Session.get(id_ + 1)
    assert Session.exist(id_)
    assert not Session.exist(id_ + 1)
    Session.destroy(id_)
    with pytest.raises(KeyError):
        Session.get(id_)
    assert not Session.exist(id_)
    Session.clear()