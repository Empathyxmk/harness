import pytest

class ConnectionId:
    def __init__(self):
        self._id = 0
        self._generation = 0

    def set_id(self, id_):
        self._id = id_

    def id(self):
        return self._id

    def set_generation(self, gen):
        self._generation = gen

    def generation(self):
        return self._generation

def test_id_set_get():
    id = ConnectionId()
    id.set_id(100002)
    assert id.id() == 100002
    id.set_generation(3)
    assert id.generation() == 3