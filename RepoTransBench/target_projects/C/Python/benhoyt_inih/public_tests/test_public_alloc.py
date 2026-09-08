import pytest
from src.inih import ini_parse_string

def ini_malloc(size):
    print(f"[pub] ini_malloc({int(size)})")
    return bytearray(size)

def ini_free(ptr):
    print("[pub] ini_free()")
    # Simulate C free()

def ini_realloc(ptr, size):
    print(f"[pub] ini_realloc({int(size)})")
    return bytearray(size)

Prev_section_public = [""]

def dumper_public(user, section, name, value):
    if section != Prev_section_public[0]:
        print(f"[pub] ... [{section}]")
        Prev_section_public[0] = section
    print(f"[pub] ... {name}={value};")
    return 1

def parse_public(name, string):
    Prev_section_public[0] = ""
    try:
        e = ini_parse_string(string, dumper_public, None)
    except NotImplementedError:
        e = 0
    print(f"{name}: e={e}")

def test_public_alloc():
    parse_public("pub_basic", "[foo]\nalice=1\nbob=2")