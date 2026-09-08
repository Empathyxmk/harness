from pypattyrn.creational.pool import Pool, Reusable
import types

class DummyReusable(Reusable):
    def __init__(self):
        self.value = 0
        super().__init__()
    def commit(self):
        # Mimic returning a snapshot/memento object.
        return {"value": self.value}
    def rollback(self, memento):
        self.value = memento["value"]

def test_pool_acquire_and_release():
    pool = Pool(DummyReusable)
    obj = pool.acquire()
    assert isinstance(obj, DummyReusable)
    obj.value = 42
    pool.release(obj)
    # When we get it again, it should be reset
    obj2 = pool.acquire()
    assert obj2.value == 0

def test_pool_expansion_when_empty():
    pool = Pool(DummyReusable)
    objs = [pool.acquire(), pool.acquire()]
    # Pool should be empty now; next acquire triggers _expand
    third = pool.acquire()
    assert isinstance(third, DummyReusable)
    assert pool.pool_size == 2

def test_reusable_reset_sets_state():
    r = DummyReusable()
    r.value = 10
    r.reset()
    assert r.value == 0

def test_pool_custom_size_args_kwargs():
    class ReusableWithArgs(Reusable):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            super().__init__()
        def commit(self):
            return {"x": self.x, "y": self.y}
        def rollback(self, memento):
            self.x = memento["x"]
            self.y = memento["y"]
    pool = Pool(ReusableWithArgs, 1, y=2)
    obj = pool.acquire()
    assert obj.x == 1 and obj.y == 2

def test_pool_release_calls_reset():
    pool = Pool(DummyReusable)
    obj = pool.acquire()
    obj.value = 222
    pool.release(obj)
    # Next acquire should be the same reset obj
    obj2 = pool.acquire()
    assert obj2.value == 0