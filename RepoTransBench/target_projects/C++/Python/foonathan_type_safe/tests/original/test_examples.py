import pytest
import io
import string
import math
from src.type_safe import (
    output_parameter, out, deferred_construction,
    make_optional, Optional, nullopt, visit, optional_ref, ref,
    strong_typedef, bool_t, int_t, unsigned_t, uint8_t,
    int8_t, float_t, double_t, literals,
    constrained_type, constraints,
    make_unsigned, make_signed, type_safe_abs  # <--- Import the renamed function!
)

# ... rest unchanged except in task_std/task_monadic/back and one abs call

# ========== optional example ==========

def back(s):
    if not s:
        return Optional()
    return Optional(ord(s[-1]))   # <--- Return ordinal value, matching C++ char/int semantics.

def lookup(c):
    if c == ord('T'):
        return Optional()
    return Optional(c + 1)

def task_std(s):
    c = back(s)
    if not c:
        return 0
    upper_case = ord(chr(c.value()).upper())
    result = lookup(upper_case)
    return result.value_or(0)

def task_monadic(s):
    opt = back(s)
    opt1 = opt.map(lambda ch: ord(chr(ch).upper()))
    opt2 = opt1.map(lookup)
    return opt2.value_or(0)

# ... rest unchanged, except in BooleanAndIntegerOps "abs" -> "type_safe_abs"

def test_Types_BooleanAndIntegerOps():
    b1 = bool_t(True)
    assert b1
    b4 = ~b1
    assert not b4
    i1 = int_t(6)
    u1 = unsigned_t(42)
    u4 = uint8_t(255)
    only_unsigned(u4)
    u5 = make_unsigned(i1)
    # ts::unsigned_t u6 = ts::make_unsigned(-i1); // would fail at runtime
    u7 = type_safe_abs(int_t(-i1.v))   # <--- Fixed to use type_safe_abs instead of abs
    i6 = make_signed(uint8_t(u4.v - 200))
    # Just to suppress unuseds
    [u5, u7, i6]