import pytest
from src.named_type.named_type import NamedType

# Test 1: Different integer value and type
class ApplesTag: pass
class Apples(NamedType[int]): pass

def test_namedtype_holds_a_different_integer():
    apples = Apples(15)
    assert apples.get() == 15

# Test 2: Different double value and custom operator
class KilometersTag: pass
class Kilometers(NamedType[float]): pass

def test_namedtype_with_double_and_addable_public():
    d1 = Kilometers(22.0)
    d2 = Kilometers(30.5)
    assert pytest.approx((d1 + d2).get()) == 52.5
    d1 += Kilometers(1.5)
    assert pytest.approx(d1.get()) == 23.5

# Test 3: Using string with different data
class SurnameTag: pass
class Surname(NamedType[str]): pass

def test_namedtype_with_string_and_comparable_public():
    s1 = Surname("Doe")
    s2 = Surname("Roe")
    assert not (s1 == s2)
    assert s1.get() < s2.get()

# Test 4: Different vector and unique value
class OddNumsTag: pass
class OddNums(NamedType[list]): pass

def test_namedtype_with_vector_public():
    v = [5, 7, 9]
    nums = OddNums(v)
    assert len(nums.get()) == 3
    assert nums.get()[1] == 7

# Test 5: Test move (Python uses assignment and copy)
class MoveTestTag: pass
class MoveTest(NamedType[str]): pass

def test_namedtype_move_constructs_and_move_assigns_properly_public():
    m1 = MoveTest("ABCD")
    m2 = m1
    assert m2.get() == "ABCD"
    m3 = MoveTest("AAAA")
    m3 = m2
    assert m3.get() == "ABCD"

# Test 6: User-defined comparison on double with different values
class StrongDoubleTag: pass
class StrongDouble(NamedType[float]): pass

def test_namedtype_comparable_skill_public():
    a = StrongDouble(21.3)
    b = StrongDouble(22.7)
    assert a != b
    assert a.get() < b.get()

# Test 7: Strong typedef for unsigned long long (simulate with int)
class KilometerNewParameter: pass
class KilometerUL(NamedType[int]): pass

def test_namedtype_with_unsigned_long_long_public():
    k1 = KilometerUL(321)
    k2 = KilometerUL(79)
    k3 = k1 + k2
    assert k3.get() == 400
    cmp = k1.get() < k3.get()
    assert cmp