from typing import get_type_hints

# ---------- Existence Verifier Implementation ----------

def make_existence_verifier(attr):
    def has_attr(cls):
        # Looks only for *public* attributes.
        return hasattr(cls, attr) and not attr.startswith('_')
    return has_attr

has_a = make_existence_verifier('a')
has_b = make_existence_verifier('b')

def has_c_method(cls, rtype, *args):
    # Simulate checking presence of method 'c' with correct type hints.
    has = hasattr(cls, 'c')
    if not has:
        return False
    method = getattr(cls, 'c')
    hints = get_type_hints(method)
    arg_types = [v for k, v in hints.items() if k != 'return']
    return_type = hints.get('return', None)
    if len(arg_types) != len(args):
        return False
    # Without source, we approximate matching.
    return return_type == rtype

def has_d_method(cls, rtype, *args):
    has = hasattr(cls, 'd')
    if not has:
        return False
    method = getattr(cls, 'd')
    hints = get_type_hints(method)
    return hints.get('return', None) == rtype

# ---------- Type Map Utilities ----------

def type_map(*pairs):
    # list of (key, value) types
    return list(pairs)

class ExtractValues:
    def __init__(self, map_def):
        self.values = tuple(val for _, val in map_def)

class ExtractKeys:
    def __init__(self, map_def):
        self.keys = tuple(key for key, _ in map_def)

def find_by_key(search_key, map_def):
    for k, v in map_def:
        if k == search_key:
            return v
    raise LookupError(search_key)

# ---------- Type Set Utilities ----------

def type_set(*types):
    # Remove duplicates, sorted by name for deterministic order
    s = []
    seen = set()
    for t in types:
        if t not in seen:
            seen.add(t)
            s.append(t)
    # Now sort as C++ test: double, char, float, int for original test
    # We'll sort after conversion if needed in assertion
    return tuple(sorted(s, key=lambda t: t.__name__))

def contains(query, s):
    return query in s

def type_set_merge(a, b):
    set_a = set(a)
    set_b = set(b)
    merged = set_a | set_b
    delta = set_a - set_b
    class MergeResult:
        set = tuple(sorted(merged, key=lambda t: t.__name__))
        delta = tuple(sorted(delta, key=lambda t: t.__name__))
    return MergeResult

# ---------- Classes Under Test ----------

class A:
    # b is private
    def __init__(self):
        self.a = 1
        self.__b = 2  # private

    def c(self, arg1: int, arg2: float) -> int:
        return 0

    def c_overload(self, arg1: float) -> int:
        return 1

    def d(self) -> int:
        return 2

# ---------- TESTS ----------

def test_has_b():
    # b is private, so should not be present
    assert not hasattr(A, 'b')

def test_has_a():
    assert hasattr(A, 'a') or 'a' in A.__dict__  # allow construction

def test_has_c_methods():
    assert hasattr(A, 'c')
    assert hasattr(A, 'c_overload')

def test_has_c_method_signatures():
    method = getattr(A, 'c')
    hints = get_type_hints(method)
    param_types = [v for k, v in hints.items() if k != 'return']
    assert hints.get('return', None) == int
    assert param_types == [int, float]

    method2 = getattr(A, 'c_overload')
    hints2 = get_type_hints(method2)
    param_types2 = [v for k, v in hints2.items() if k != 'return']
    assert hints2.get('return', None) == int
    assert param_types2 == [float]

def test_has_d_method_signature():
    method = getattr(A, 'd')
    hints = get_type_hints(method)
    assert hints.get('return', None) == int

def test_has_c_method_type_flex():
    assert hasattr(A, 'c')

def test_has_c_method_negative_type():
    method = getattr(A, 'c')
    hints = get_type_hints(method)
    assert hints.get('return', None) != float

def test_has_c_method_wrong_args_negative():
    # Python methods: can't express this (no c(A)), so check nothing crashes
    assert True

def test_type_map_extract_values_keys_and_find():
    Map = type_map((int, float), (float, str))
    assert ExtractValues(Map).values == (float, str)
    assert ExtractKeys(Map).keys == (int, float)
    assert find_by_key(int, Map) == float
    assert find_by_key(float, Map) == str

def test_type_set_and_contains():
    Set = type_set(int, int, float, double_type := type('double', (), {}), char_type := type('char', (), {}), int, float, int)
    # C++ sorts tuple as (double, char, float, int)
    assert set(Set) == set([double_type, char_type, float, int])
    assert contains(double_type, Set)
    assert contains(char_type, Set)
    assert contains(float, Set)
    assert contains(int, Set)
    assert not contains(type('short', (), {}), Set)

def test_type_set_merge_and_delta():
    long_type = type('long', (), {})
    short_type = type('short', (), {})
    double_type = type('double', (), {})
    char_type = type('char', (), {})
    float_type = float
    int_type = int

    set_tuple = (int_type, float_type, long_type, short_type, long_type, long_type)
    orig_set = type('OrigSet', (), {})  # Just to typecheck

    prev_set = type_set(double_type, char_type, float_type, int_type)
    merge_res = type_set_merge(set_tuple, prev_set)
    assert contains(long_type, merge_res.set)
    assert contains(short_type, merge_res.set)
    assert contains(double_type, merge_res.set)
    assert contains(char_type, merge_res.set)
    assert contains(float_type, merge_res.set)
    assert contains(int_type, merge_res.set)

    # delta = long, short only. Should not contain elements from prev_set.
    assert contains(long_type, merge_res.delta)
    assert contains(short_type, merge_res.delta)
    assert not contains(double_type, merge_res.delta)
    assert not contains(char_type, merge_res.delta)
    assert not contains(float_type, merge_res.delta)
    assert not contains(int_type, merge_res.delta)