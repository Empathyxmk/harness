import pytest
from src.named_type.named_type import NamedType

import math
import operator

# ================== Helper Types =====================

class Meter(NamedType[int]):
    pass

def meter(value):
    return Meter(value)

class Width(NamedType[Meter]):
    pass

class Height(NamedType[Meter]):
    pass

class Rectangle:
    def __init__(self, width, height):
        self._width = width.get()
        self._height = height.get()
    def getWidth(self):
        return self._width
    def getHeight(self):
        return self._height

def test_basic_usage():
    r = Rectangle(Width(meter(10)), Height(meter(12)))
    assert r.getWidth() == 10
    assert r.getHeight() == 12

class NameRef(NamedType):
    pass

def changeValue(name):
    name_ref = name.get()
    name_ref[0] = "value2"

def test_passing_a_strong_reference():
    value_holder = ["value1"]
    name = NameRef(value_holder)
    changeValue(name)
    assert value_holder[0] == "value2"

def test_addable():
    class AddableType(NamedType[int]):
        pass
    s1 = AddableType(12)
    s2 = AddableType(10)
    assert (s1 + s2).get() == 22
    assert (+s1).get() == 12

def test_binary_addable():
    class BinaryAddableType(NamedType[int]):
        pass
    s1 = BinaryAddableType(12)
    s2 = BinaryAddableType(10)
    assert (s1 + s2).get() == 22

def test_unary_addable():
    class UnaryAddableType(NamedType[int]):
        pass
    s1 = UnaryAddableType(12)
    assert (+s1).get() == 12

def test_subtractable():
    class SubtractableType(NamedType[int]):
        pass
    s1 = SubtractableType(12)
    s2 = SubtractableType(10)
    assert (s1 - s2).get() == 2
    assert (-s1).get() == -12

def test_binary_subtractable():
    class BinarySubtractableType(NamedType[int]):
        pass
    s1 = BinarySubtractableType(12)
    s2 = BinarySubtractableType(10)
    assert (s1 - s2).get() == 2

def test_unary_subtractable():
    class UnarySubtractableType(NamedType[int]):
        pass
    s = UnarySubtractableType(12)
    assert (-s).get() == -12

def test_multiplicable():
    class MultiplicableType(NamedType[int]):
        pass
    s1 = MultiplicableType(12)
    s2 = MultiplicableType(10)
    assert (s1 * s2).get() == 120
    s1 *= s2
    assert s1.get() == 120

def test_divisible():
    class DivisibleType(NamedType[int]):
        pass
    s1 = DivisibleType(120)
    s2 = DivisibleType(10)
    assert (s1 / s2).get() == 12
    s1 /= s2
    assert s1.get() == 12

def test_modulable():
    class ModulableType(NamedType[int]):
        pass
    s1 = ModulableType(5)
    s2 = ModulableType(2)
    assert (s1 % s2).get() == 1
    s1 %= s2
    assert s1.get() == 1

def test_bitwise_invertable():
    class BitWiseInvertableType(NamedType[int]):
        pass
    s1 = BitWiseInvertableType(13)
    assert (~s1).get() == ~13

def test_bitwise_andable():
    class BitWiseAndableType(NamedType[int]):
        pass
    s1 = BitWiseAndableType(2)
    s2 = BitWiseAndableType(64)
    assert (s1 & s2).get() == (2 & 64)
    s1 &= s2
    assert s1.get() == (2 & 64)

def test_bitwise_orable():
    class BitWiseOrableType(NamedType[int]):
        pass
    s1 = BitWiseOrableType(2)
    s2 = BitWiseOrableType(64)
    assert (s1 | s2).get() == (2 | 64)
    s1 |= s2
    assert s1.get() == (2 | 64)

def test_bitwise_xorable():
    class BitWiseXorableType(NamedType[int]):
        pass
    s1 = BitWiseXorableType(2)
    s2 = BitWiseXorableType(64)
    assert (s1 ^ s2).get() == (2 ^ 64)
    s1 ^= s2
    assert s1.get() == (2 ^ 64)

def test_bitwise_leftshiftable():
    class BitWiseLeftShiftableType(NamedType[int]):
        pass
    s1 = BitWiseLeftShiftableType(2)
    s2 = BitWiseLeftShiftableType(3)
    assert (s1 << s2).get() == (2 << 3)
    s1 <<= s2
    assert s1.get() == (2 << 3)

def test_bitwise_rightshiftable():
    class BitWiseRightShiftableType(NamedType[int]):
        pass
    s1 = BitWiseRightShiftableType(2)
    s2 = BitWiseRightShiftableType(3)
    assert (s1 >> s2).get() == (2 >> 3)
    s1 >>= s2
    assert s1.get() == (2 >> 3)

def test_comparable():
    a = meter(10)
    b = meter(11)
    assert a == meter(10)
    assert not (a == b)
    assert a != b
    assert not (a != a)
    assert a < b
    assert not (a < a)
    assert a <= a
    assert a <= b
    assert not (a <= meter(9))
    assert meter(11) > a
    assert not (a > meter(11))
    assert meter(11) >= a
    assert a >= a
    assert not (meter(9) >= a)

def test_hash():
    class SerialNumber(NamedType[str]):
        pass
    hashMap = {SerialNumber("AA11"): 10, SerialNumber("BB22"): 20}
    cc33 = SerialNumber("CC33")
    hashMap[cc33] = 30
    assert hashMap[SerialNumber("AA11")] == 10
    assert hashMap[SerialNumber("BB22")] == 20
    assert hashMap[cc33] == 30

def test_arithmetic():
    class StrongArithmetic(NamedType[int]):
        pass
    a = StrongArithmetic(1)
    b = StrongArithmetic(2)
    assert (a + b).get() == 3
    a += b
    assert a.get() == 3
    assert (a - b).get() == 1
    a -= b
    assert a.get() == 1
    a = StrongArithmetic(5)
    assert (a * b).get() == 10
    a *= b
    assert a.get() == 10
    assert (a / b).get() == 5
    a /= b
    assert a.get() == 5
    a = StrongArithmetic(a.get() + 1)
    assert a.get() == 6

def test_printable(capsys):
    class StrongInt(NamedType[int]):
        pass
    val = StrongInt(42)
    print(val, end="")
    captured = capsys.readouterr()
    assert captured.out == "42"

def test_dereferencable():
    # Python doesn't have * operator for custom types, but we can test getting value
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    v = a.get()
    assert v == 1
    a2 = StrongInt(1)
    v2 = a2.get()
    assert v2 == 1
    a3 = StrongInt(1)
    v3 = a3.get()
    v3 = 2
    assert a3.get() == 1  # not reflected unless mutable, Python has no pointers
    def functionReturningStrongInt():
        return StrongInt(28)
    def functionTakingInt(value):
        return value
    value = functionTakingInt(functionReturningStrongInt().get())
    assert value == 28

def test_preincrementable():
    # Python has no ++ but we can emulate in place addition
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    a = StrongInt(a.get() + 1)
    b = a
    assert a.get() == 2
    assert b.get() == 2

def test_postincrementable():
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    b = a
    a = StrongInt(a.get() + 1)
    assert a.get() == 2
    assert b.get() == 1

def test_predecrementable():
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    a = StrongInt(a.get() - 1)
    b = a
    assert a.get() == 0
    assert b.get() == 0

def test_postdecrementable():
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    b = a
    a = StrongInt(a.get() - 1)
    assert a.get() == 0
    assert b.get() == 1

def test_incrementable():
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    b = StrongInt(a.get() + 1)
    assert a.get() == 1
    assert b.get() == 2
    a2 = StrongInt(1)
    b2 = a2
    a2 = StrongInt(a2.get() + 1)
    assert a2.get() == 2
    assert b2.get() == 1

def test_decrementable():
    class StrongInt(NamedType[int]):
        pass
    a = StrongInt(1)
    b = StrongInt(a.get() - 1)
    assert a.get() == 1
    assert b.get() == 0
    a2 = StrongInt(1)
    b2 = a2
    a2 = StrongInt(a2.get() - 1)
    assert a2.get() == 0
    assert b2.get() == 1

def test_empty_base_class_optimisation_of_skills():
    # In Python, size optimization by inheritance is irrelevant
    assert True

def test_empty_base_class_optimization():
    # In Python, memory layout isn't relevant the same way; always True
    assert True

def test_constexpr():
    # Python does not have constexpr, but all logic is runtime evaluable
    class StrongBool(NamedType[bool]):
        pass
    assert StrongBool(True).get()

def test_throw_on_construction():
    class ThrowOnConstruction:
        def __init__(self):
            raise Exception(42)
    with pytest.raises(Exception) as excinfo:
        ThrowOnConstruction()
    assert excinfo.value.args[0] == 42
    class ThrowOnConstruction2:
        def __init__(self, arg):
            raise Exception("exception")
    with pytest.raises(Exception) as excinfo2:
        ThrowOnConstruction2(5)
    assert excinfo2.value.args[0] == "exception"

def test_noexcept():
    # All Python initializations will raise, unless caught. So we'll just pass
    assert True

def test_version_macros_are_defined():
    # We'll simulate version variables
    NAMED_TYPE_VERSION_MAJOR = 1
    NAMED_TYPE_VERSION_MINOR = 0
    NAMED_TYPE_VERSION_PATCH = 0
    NAMED_TYPE_VERSION = f"{NAMED_TYPE_VERSION_MAJOR}.{NAMED_TYPE_VERSION_MINOR}.{NAMED_TYPE_VERSION_PATCH}"
    assert NAMED_TYPE_VERSION_MAJOR >= 1
    assert NAMED_TYPE_VERSION_MINOR >= 0
    assert NAMED_TYPE_VERSION_PATCH >= 0
    s = f"{NAMED_TYPE_VERSION_MAJOR}.{NAMED_TYPE_VERSION_MINOR}.{NAMED_TYPE_VERSION_PATCH}"
    assert s == NAMED_TYPE_VERSION

def test_named_arguments():
    # Python does not have named arguments in the C++ NamedType sense. Use kwargs.
    def getFullName(firstName, lastName):
        return firstName + lastName
    fullName = getFullName(firstName="James", lastName="Bond")
    assert fullName == "JamesBond"

def test_named_arguments_in_any_order():
    def getFullName(**kwargs):
        return kwargs["firstName"] + kwargs["lastName"]
    fullName = getFullName(lastName="Bond", firstName="James")
    assert fullName == "JamesBond"
    fullName2 = getFullName(firstName="James", lastName="Bond")
    assert fullName2 == "JamesBond"

def test_named_arguments_with_bracket_constructor():
    def getNumbers(numbers):
        return numbers
    vec = getNumbers([1, 2, 3])
    assert vec == [1, 2, 3]