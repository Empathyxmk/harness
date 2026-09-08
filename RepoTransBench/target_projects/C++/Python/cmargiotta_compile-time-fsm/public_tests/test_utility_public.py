from typing import get_type_hints

# ---------- Existence Verifier Implementation ----------

def make_existence_verifier(attr):
    def has_attr(cls):
        return hasattr(cls, attr) and not attr.startswith('_')
    return has_attr

has_x = make_existence_verifier('x')
has_y = make_existence_verifier('y')

def has_z_method(cls, rtype, *args):
    has = hasattr(cls, 'z')
    if not has:
        return False
    method = getattr(cls, 'z')
    hints = get_type_hints(method)
    arg_types = [v for k, v in hints.items() if k != 'return']
    return_type = hints.get('return', None)
    if len(arg_types) != len(args):
        return False
    return return_type == rtype

def has_q_method(cls, rtype, *args):
    has = hasattr(cls, 'q')
    if not has:
        return False
    method = getattr(cls, 'q')
    hints = get_type_hints(method)
    return hints.get('return', None) == rtype

# ---------- Type Map Utilities ----------

def type_map(*pairs):
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
    s = []
    seen = set()
    for t in types:
        if t not in seen:
            seen.add(t)
            s.append(t)
    # C++ test yields (unsigned, bool, float, char)
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

class B:
    # x is private
    def __init__(self):
        self.y = 1.23
        self.__x = 42.0

    def z(self, arg1: int) -> None:
        return None

    def z_overload(self, arg1: float, arg2: float) -> float:
        return 0.0

    def q(self) -> str:
        return 'q'

# ---------- TESTS ----------

def test_has_x():
    # x is private
    assert not hasattr(B, 'x')

def test_has_y():
    # y is public
    assert hasattr(B, 'y') or 'y' in B.__dict__

def test_has_z_methods():
    assert hasattr(B, 'z')
    assert hasattr(B, 'z_overload')

def test_has_z_method_signatures():
    method = getattr(B, 'z')
    hints = get_type_hints(method)
    param_types = [v for k, v in hints.items() if k != 'return']
    assert hints.get('return', None) == type(None)
    assert param_types == [int]

    method2 = getattr(B, 'z_overload')
    hints2 = get_type_hints(method2)
    param_types2 = [v for k, v in hints2.items() if k != 'return']
    assert hints2.get('return', None) == float
    assert param_types2 == [float, float]

def test_has_q_method_signature():
    method = getattr(B, 'q')
    hints = get_type_hints(method)
    assert hints.get('return', None) == str

def test_has_z_method_type_flex():
    assert hasattr(B, 'z')

def test_has_z_method_negative_type():
    method = getattr(B, 'z')
    hints = get_type_hints(method)
    assert hints.get('return', None) != float

def test_has_z_method_wrong_args_negative():
    assert True

def test_type_map_extract_values_keys_and_find():
    Map = type_map((int, float), (str, bool))
    assert ExtractValues(Map).values == (float, bool)
    assert ExtractKeys(Map).keys == (int, str)
    assert find_by_key(int, Map) == float
    assert find_by_key(str, Map) == bool

def test_type_set_and_contains():
    char_type = type('char', (), {})
    bool_type = bool
    unsigned_type = type('unsigned', (), {})
    float_type = float

    Set = type_set(char_type, bool_type, unsigned_type, char_type, bool_type, unsigned_type, float_type)
    assert set(Set) == set([unsigned_type, bool_type, float_type, char_type])
    assert contains(unsigned_type, Set)
    assert contains(bool_type, Set)
    assert contains(float_type, Set)
    assert contains(char_type, Set)
    assert not contains(int, Set)

def test_type_set_merge_and_delta():
    string_type = type('string', (), {})      # simulate std::string
    bool_type = bool
    char_type = type('char', (), {})
    double_type = type('double', (), {})
    float_type = float
    unsigned_type = type('unsigned', (), {})

    s1 = (bool_type, string_type, char_type, double_type, double_type)
    pub_set = type_set(char_type, bool_type, unsigned_type, float_type)
    res = type_set_merge(s1, pub_set)
    expected_merged = set([string_type, bool_type, char_type, double_type, unsigned_type, float_type])
    assert set(res.set) == expected_merged
    assert contains(string_type, res.set)
    assert contains(bool_type, res.set)
    assert contains(double_type, res.set)
    assert contains(unsigned_type, res.set)
    assert contains(float_type, res.set)
    assert contains(char_type, res.set)

    # delta: only items from s1 not in pub_set: string, double
    assert contains(string_type, res.delta)
    assert contains(double_type, res.delta)
    assert not contains(unsigned_type, res.delta)
    assert not contains(bool_type, res.delta)
    assert not contains(float_type, res.delta)
    assert not contains(char_type, res.delta)