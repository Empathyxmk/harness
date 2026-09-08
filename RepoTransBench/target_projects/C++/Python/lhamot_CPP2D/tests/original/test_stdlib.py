import pytest
import math
import io

def test_std_map_typing():
    # Just test that we can create mappings of correct type and value
    m1 = dict()
    m1[36] = 78
    assert m1[36] == 78
    m2 = dict(m1)
    m2[36] = 581
    assert m2[36] == 581
    assert m1[36] == 78
    tutu = dict()
    titi = (0, '')
    tata = [dict()]

def test_containhashmap_classes():
    class ContainHashMap:
        def __init__(self):
            self.m1 = {}
    class ContainHashMap2:
        def __init__(self):
            self.m1 = {}
        def __copy__(self):
            new = ContainHashMap2()
            new.m1 = self.m1.copy()
            return new
    class ContainHashMap3:
        def __init__(self):
            self.m1 = {}
        def __copy__(self):
            new = ContainHashMap3()
            new.m1 = self.m1.copy()
            return new
    for cls in [ContainHashMap, ContainHashMap2, ContainHashMap3]:
        c1 = cls()
        c1.m1[15] = 98
        from copy import copy
        c2 = copy(c1)
        c1.m1[15] = 6
        assert c2.m1[15] == 98
        c2 = copy(c1)
        c1.m1[15] = 7
        assert c2.m1[15] == 6

def test_cmath():
    assert math.sqrt(4.0) == 2.0
    assert math.pow(2, 2) == 4

def test_std_unordered_map_behavior():
    m1 = dict()
    m1[36] = 78
    assert m1[36] == 78
    v1 = []
    v2 = []
    for k, v in m1.items():
        v1.append(k)
        v2.append(v)
    assert v1[0] == 36
    assert v2[0] == 78
    # ContainHashMap test
    class ContainHashMap:
        def __init__(self):
            self.m1 = {}
    c1 = ContainHashMap()
    c1.m1[15] = 98
    from copy import deepcopy
    c2 = deepcopy(c1)
    c1.m1[15] = 6
    assert c2.m1[15] == 98
    c2 = deepcopy(c1)
    c1.m1[15] = 7
    assert c2.m1[15] == 6
    # ContainHashMap2 test
    class ContainHashMap2:
        def __init__(self):
            self.m1 = {}
        def __copy__(self):
            new = ContainHashMap2()
            new.m1 = self.m1.copy()
            return new
    c1 = ContainHashMap2()
    c1.m1[15] = 98
    from copy import copy
    c2 = copy(c1)
    c1.m1[15] = 6
    assert c2.m1[15] == 98
    c2 = copy(c1)
    c1.m1[15] = 7
    assert c2.m1[15] == 6
    # ContainHashMap3 test
    class ContainHashMap3:
        def __init__(self):
            self.m1 = {}
        def __copy__(self):
            new = ContainHashMap3()
            new.m1 = self.m1.copy()
            return new
    c1 = ContainHashMap3()
    c1.m1[15] = 98
    c2 = copy(c1)
    c1.m1[15] = 6
    assert c2.m1[15] == 98
    c2 = copy(c1)
    c1.m1[15] = 7
    assert c2.m1[15] == 6

def test_shared_ptr_simulation():
    class Class781:
        def __init__(self, i=0):
            self.i = i
    class Struct781:
        def __init__(self, i=0):
            self.i = i
    # Simulate shared_ptr as plain references
    classptr1 = None
    assert classptr1 is None
    classptr1 = Class781()
    assert classptr1 is not None
    classptr2 = classptr1
    assert classptr1 is classptr2
    classptr4 = Class781()
    assert classptr4 is not None
    classptr4 = Class781()
    assert classptr4 is not None
    classptr4 = classptr2
    assert classptr4 is classptr2
    structptr1 = None
    assert structptr1 is None
    structptr1 = Struct781()
    assert structptr1 is not None
    structptr2 = structptr1
    assert structptr2 is structptr1
    structptr4 = Struct781()
    assert structptr4 is not None
    structptr4 = structptr1
    assert structptr4 is structptr1

def test_unique_ptr_simulation():
    class Class781:
        def __init__(self, i=0):
            self.i = i
    class Struct781:
        def __init__(self, i=0):
            self.i = i
    classptr1 = None
    assert classptr1 is None
    classptr1 = Class781()
    assert classptr1 is not None
    classptr2 = classptr1
    assert classptr2 is not None
    classptr1 = None
    assert classptr1 is None
    classptr4 = Class781()
    classptr4.i = 78
    assert classptr4.i == 78
    assert classptr4 is not None
    classptr4 = Class781()
    assert classptr4 is not None
    classptr4 = classptr2
    assert classptr4 is not None
    assert classptr2 is not None
    structptr1 = None
    assert structptr1 is None
    structptr1 = Struct781()
    structptr1.i = 78
    assert structptr1.i == 78
    assert structptr1 is not None
    structptr2 = structptr1
    assert structptr2 is not None
    structptr1 = None
    assert structptr1 is None
    structptr4 = Struct781()
    assert structptr4 is not None
    structptr4 = structptr2
    assert structptr4 is not None
    assert structptr2 is not None

def test_stdarray():
    a = [2] * 4
    assert a[3] == 2
    b = [0, 1, 2, 3]
    assert b[1] == 1

def test_stdpair():
    p1 = [None, None]
    p1[0] = 3
    p1[1] = 3.141
    assert p1[0] == 3
    assert abs(p1[1] - 3.141) < 1e-8
    p2 = [4, 4.44444]
    assert p2[0] == 4
    p3 = [6, 6.66666]
    assert p3[0] == 6
    p1[0] = 7
    assert p1[0] == 7

def test_vector_types():
    class Class781:
        def __init__(self, i=0):
            self.i = i
    class Class783(Class781):
        def __init__(self):
            super().__init__(12)
    class Struct781:
        def __init__(self, i=0):
            self.i = i
    a = []
    a.append(2)
    assert a[0] == 2
    assert len(a) == 1
    class Blu:
        A1 = 1
    b = []
    b.append(Blu.A1)
    assert b[0] == Blu.A1
    assert len(b) == 1
    c = []
    c.append(Struct781())
    assert c[0].i == 0
    assert len(c) == 1
    d = []
    d.append(Class781())
    assert d[0].i == 0
    assert len(d) == 1
    d.append(Class783())
    assert d[1].i == 12
    assert d[1].i == 12
    assert len(d) == 2

def test_tuple_behavior():
    # tuple with int and dict
    tutu = (42, "azer")
    assert tutu[0] == 42
    assert tutu[1] == "azer"
    # Python doesn't need tuple of reference, skip

def test_stringstream_behavior():
    ss = io.StringIO()
    ss.write("abc")
    ss.write(" ")
    ss.write(str(42))
    assert ss.getvalue() == "abc 42"
    ss2 = ss
    assert ss2.getvalue() == "abc 42"
    ss3 = io.StringIO("dfgdfgfh")
    assert ss3.getvalue() == "dfgdfgfh"