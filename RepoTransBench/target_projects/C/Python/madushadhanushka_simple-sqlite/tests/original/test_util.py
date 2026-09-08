import pytest

# Placeholder stubs, to be replaced by your actual core/util implementation
class UtilMemoryState:
    # Simulate a global malloc_failed flag
    sqlite_malloc_failed = 0

def sqliteMalloc(size):
    assert size >= 0
    return bytearray(size) if size > 0 else bytearray(1)

def sqliteFree(p):
    pass

def sqliteSetString(dest, *args):
    result = ''
    i = 0
    # Accept only positional args (and ignore dest, simulate C-style)
    while i < len(args) and args[i] is not None:
        result += args[i]
        i += 1
    # mimic allocation & assignment via return value
    return result

def sqliteHashNoCase(z, n):
    # Dummy hash implementation: sum of lower() chars
    s = z[:n] if n >= 0 else z
    return sum(ord(c.lower()) for c in s) or 1

sqlite_malloc_failed = 0

def test_sqlite_alloc():
    p = sqliteMalloc(32)
    assert p is not None
    for i in range(32):
        p[i] = 1
    sqliteFree(p)

def test_sqlite_malloc_failed():
    global sqlite_malloc_failed
    old_failed = sqlite_malloc_failed
    p = sqliteMalloc(0)  # Should not fail, returns not None
    assert p is not None
    sqliteFree(p)
    assert sqlite_malloc_failed == old_failed

def test_sqliteSetString():
    z = sqliteSetString(None, "Hello", " ", "World", None)
    assert z is not None
    assert z == "Hello World"

    y = sqliteSetString(None, "A", None)
    assert y is not None
    assert y == "A"

    # Should not error with NULL dest pointer -- here, None is handled
    sqliteSetString(None, "Anything", None)

def test_sqliteHashNoCase():
    h1 = sqliteHashNoCase("TEST", -1)
    h2 = sqliteHashNoCase("test", -1)
    assert h1 == h2

    h3 = sqliteHashNoCase("Hash", 4)
    assert h3 > 0

def test_sqliteHashNoCase_len0():
    h = sqliteHashNoCase("Ignored", 0)
    assert h > 0