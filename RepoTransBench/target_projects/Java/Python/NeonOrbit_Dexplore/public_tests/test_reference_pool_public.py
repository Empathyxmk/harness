def s(s): 
    return StringRefData(s)
def t(s):
    return TypeRefData(s)
def f(n):
    return FieldRefData(n)
def m(n):
    return MethodRefData(n)

class StringRefData:
    @staticmethod
    def build(val): return StringRefData(val)
    def __init__(self, s): self._s = s
    def getString(self): return self._s
class TypeRefData:
    @staticmethod
    def build(val): return TypeRefData(val)
    def __init__(self, t): self._t = t
    def getType(self): return self._t
class FieldRefData:
    @staticmethod
    def build(val, _): return FieldRefData(val)
    def __init__(self, n): self._n = n
    def getName(self): return self._n
class MethodRefData:
    @staticmethod
    def build(val, _): return MethodRefData(val)
    def __init__(self, n): self._n = n
    def getName(self): return self._n

class ReferencePool:
    @staticmethod
    def build(strings, types, fields, methods):
        if not (strings or types or fields or methods):
            return ReferencePool.emptyPool()
        return ReferencePool(strings, types, fields, methods)
    @staticmethod
    def merge(pools):
        pools = [p for p in pools if not p.isEmpty()]
        if not pools:
            return ReferencePool.emptyPool()
        s = []
        t = []
        f = []
        m = []
        for pool in pools:
            s += pool.getStringSection()
            t += pool.getTypeSection()
            f += pool.getFieldSection()
            m += pool.getMethodSection()
        return ReferencePool(s, t, f, m)
    @staticmethod
    def emptyPool():
        if not hasattr(ReferencePool, '_EMPTY'):
            ReferencePool._EMPTY = ReferencePool([], [], [], [])
        return ReferencePool._EMPTY
    def __init__(self, strings, types, fields, methods):
        self._strings = strings
        self._types = types
        self._fields = fields
        self._methods = methods
    def getStringSection(self): return self._strings
    def getTypeSection(self): return self._types
    def getFieldSection(self): return self._fields
    def getMethodSection(self): return self._methods
    def isEmpty(self): return (not self._strings and
                              not self._types and
                              not self._fields and
                              not self._methods)

def test_reference_pool_empty_public():
    empty1 = ReferencePool.build([], [], [], [])
    empty2 = ReferencePool.emptyPool()
    assert empty1 is empty2
    assert empty1.isEmpty()
    assert empty2.isEmpty()
    assert len(empty1.getStringSection()) == 0

def test_reference_pool_non_empty_public():
    strings = [s("abc"), s("def")]
    types = [t("ty")]
    fields = [f("sf")]
    methods = [m("sm")]

    pool = ReferencePool.build(strings, types, fields, methods)
    assert pool is not ReferencePool.emptyPool()
    assert not pool.isEmpty()
    assert len(pool.getStringSection()) == 2
    assert pool.getStringSection()[0].getString() == "abc"
    assert pool.getTypeSection()[0].getType() == "ty"
    assert pool.getFieldSection()[0].getName() == "sf"
    assert pool.getMethodSection()[0].getName() == "sm"

def test_reference_pool_merge_public():
    p1 = ReferencePool.build([s("s1")], [], [], [])
    p2 = ReferencePool.build([], [t("T2")], [], [])
    p3 = ReferencePool.emptyPool()
    pools = [p1, p2, p3]
    merged = ReferencePool.merge(pools)
    assert not merged.isEmpty()
    assert merged.getStringSection()[0].getString() == "s1"
    assert merged.getTypeSection()[0].getType() == "T2"
    assert len(merged.getFieldSection()) == 0

def test_reference_pool_merge_all_empty_public():
    e1 = ReferencePool.emptyPool()
    e2 = ReferencePool.emptyPool()
    assert ReferencePool.emptyPool() is ReferencePool.merge([e1, e2])