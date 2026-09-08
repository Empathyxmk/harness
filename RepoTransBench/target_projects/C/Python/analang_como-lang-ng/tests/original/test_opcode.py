import pytest
from src.como_lang.mocks import ComoOpCode, INONE, LOAD_CONST, instrstr, objectToString

def test_instrstr_no_operand():
    op = ComoOpCode(op_code=INONE, operand=None)
    s = instrstr(op)
    assert s.startswith("INONE ")
    assert objectToString(None) in s # Ensure operand is correctly represented as "NULL"

def test_instrstr_with_operand():
    dummy = object() # Use a Python object to simulate C's void*
    op = ComoOpCode(op_code=LOAD_CONST, operand=dummy)
    s = instrstr(op)
    assert "LOAD_CONST" in s
    assert objectToString(dummy) in s # Ensure operand is correctly represented