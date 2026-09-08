import pytest

class TestCounter:
    count = 0
    def __init__(self):
        TestCounter.count += 1
    def __del__(self):
        TestCounter.count -= 1

class DummyRef:
    """Naive SharedPtr/UniquePtr tracker using refcounts"""
    def __init__(self, obj):
        self.obj = obj
        self.count = 1
    def clone(self):
        self.count += 1
        return self
    def release(self):
        self.count -= 1

class SharedPtr:
    def __init__(self, obj=None):
        self.obj = obj
        self.ref = DummyRef(obj) if obj else None
    def __bool__(self):
        return self.ref is not None and self.ref.count > 0
    def use_count(self):
        if self.ref:
            return self.ref.count
        return 0
    def __del__(self):
        if self.ref:
            self.ref.release()
            if self.ref.count == 0:
                del self.obj
    def reset(self):
        if self.ref:
            self.ref.release()
        self.ref = None
        self.obj = None
    # Copying increments count (simulating)
    def __copy__(self):
        if self.ref:
            self.ref.clone()
        return SharedPtr(self.obj)
    def __deepcopy__(self, memodict={}):
        if self.ref:
            self.ref.clone()
        return SharedPtr(self.obj)
    def __eq__(self, other):
        return self.obj == other.obj

def MakeShared(val):
    return SharedPtr(val)

class UniquePtr:
    def __init__(self, val):
        self.val = val
    def move(self):
        v = self.val
        self.val = None
        return v

def test_basic_shared():
    TestCounter.count = 0
    sp = SharedPtr(TestCounter())
    assert TestCounter.count == 1
    sp2 = sp
    # The same TestCounter obj
    assert TestCounter.count == 1
    assert sp2.use_count() == sp.use_count()
    # Drop reference
    del sp
    # Reference should still be present due to sp2
    # TestCounter not deleted until all gone
    assert TestCounter.count == 1
    del sp2
    # After GC, count becomes zero (depends on collection timing, force it)
    import gc; gc.collect()
    assert TestCounter.count == 0

def test_reset_and_null():
    s1 = SharedPtr(42)
    s1.reset()
    assert not s1
    s2 = SharedPtr()
    assert not s2

def test_make_shared():
    sp = MakeShared(99)
    assert sp.__bool__()

def test_unique_conversion():
    uptr = UniquePtr(55)
    sp = SharedPtr(uptr.move())
    assert sp.obj == 55