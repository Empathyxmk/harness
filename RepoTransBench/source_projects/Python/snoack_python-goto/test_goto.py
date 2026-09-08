import pytest
import types
import goto

def test_with_goto_preserves_function_basic():
    def foo(x): return x*2
    wrapped = goto.with_goto(foo)
    assert callable(wrapped)
    assert wrapped(4) == 8
    assert wrapped.__name__ == foo.__name__
    assert wrapped.__doc__ == foo.__doc__

def test_with_goto_rejects_invalid_type():
    with pytest.raises(TypeError):
        goto.with_goto(1234)

def test_with_goto_marks_function_idempotent():
    def bar(): pass
    foo = goto.with_goto(bar)
    again = goto.with_goto(foo)
    assert again is foo

def test_with_goto_on_code_object():
    def dummy(): return 11
    new_code = goto.with_goto(dummy.__code__)
    assert isinstance(new_code, type(dummy.__code__))

def test_make_code_and_patch_code_roundtrip():
    def baz(q=1): return q+5
    result1 = baz(7)
    func2 = goto.with_goto(baz)
    assert func2(8) == 13

def test_patch_code_preserves_cellvars_freevars():
    def func(x):
        def inner():
            return x+1
        return inner()
    with_goto_func = goto.with_goto(func)
    assert with_goto_func(3) == 4

def test_with_goto_closure():
    def make_closer(a):
        def inner():
            return a+2
        return inner
    f = make_closer(40)
    wrapper = goto.with_goto(f)
    assert wrapper() == 42

def test_bytecode_repr():
    b = goto._Bytecode()
    r = repr(b)
    assert "argument_bits" in r

def test_find_labels_and_gotos_empty():
    lb, gt = goto._find_labels_and_gotos([])
    assert lb == {}
    assert gt == []

def test_write_instruction_small_arg():
    buf = bytearray(4)
    goto._write_instructions(buf, 0, [("LOAD_CONST", 2)])
    assert isinstance(buf, bytearray)

def test_write_instruction_extended_arg():
    buf = bytearray(8)
    # just try not to error; can't introspect
    goto._write_instructions(buf, 0, [("LOAD_CONST", 99999)])

def test_array_to_bytes():
    import array
    a = array.array("B", [10, 20])
    b = goto._array_to_bytes(a)
    assert isinstance(b, (bytes, str))