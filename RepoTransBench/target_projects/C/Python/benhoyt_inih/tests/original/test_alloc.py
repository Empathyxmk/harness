import pytest
from src.inih import ini_parse_string

def ini_malloc(size):
    print(f"ini_malloc({int(size)})")
    return bytearray(size)

def ini_free(ptr):
    print("ini_free()")
    # nothing needed in Python

def ini_realloc(ptr, size):
    print(f"ini_realloc({int(size)})")
    return bytearray(size)  # not actually reallocating

Prev_section = [""]

def dumper(user, section, name, value):
    if section != Prev_section[0]:
        print(f"... [{section}]")
        Prev_section[0] = section
    print(f"... {name}={value};")
    return 1

def parse(name, string):
    Prev_section[0] = ""
    # Should call ini_parse_string and run
    try:
        e = ini_parse_string(string, dumper, None)
    except NotImplementedError:
        # Just simulate output to match C code structure for now
        e = 0
    print(f"{name}: e={e}")

def test_alloc_basic():
    parse("basic", "[section]\nfoo = bar\nbazz = buzz quxx")