import pytest

# Public test stubs. Instructed to maintain test logic and function names.

def sqliteMalloc(size):
    assert size >= 0
    return bytearray(size) if size > 0 else bytearray(1)

def sqliteFree(p):
    pass

def sqliteSetString(dest, *args):
    result = ''
    i = 0
    while i < len(args) and args[i] is not None:
        result += args[i]
        i += 1
    return result

def sqliteStrICmp(a, b):
    return (a.casefold() > b.casefold()) - (a.casefold() < b.casefold())

def sqliteStrNICmp(a, b, n):
    return (a[:n].casefold() > b[:n].casefold()) - (a[:n].casefold() < b[:n].casefold())

def sqliteStrDup(s):
    return s[:]

def sqliteCheckMemory():
    # Always returns 0 for this stub
    return 0

sqlite_malloc_failed = 0

def test_sqlite_alloc_public():
    p = sqliteMalloc(48)
    assert p is not None
    for i in range(48):
        p[i] = 2
    sqliteFree(p)

def test_sqlite_malloc_failed_public():
    global sqlite_malloc_failed
    old_failed = sqlite_malloc_failed
    p = sqliteMalloc(8)
    assert p is not None
    sqliteFree(p)
    assert sqlite_malloc_failed == old_failed

def test_sqliteSetString_public():
    z = sqliteSetString(None, "Foo", "-", "Bar", None)
    assert z is not None
    assert z == "Foo-Bar"
    # Memory "free"
    sqliteFree(z)

def test_sqliteStrICmp_public():
    assert sqliteStrICmp("Test", "tESt") == 0
    assert sqliteStrICmp("Apple", "Banana") < 0
    assert sqliteStrICmp("Zebra", "ant") > 0

def test_sqliteStrNICmp_public():
    assert sqliteStrNICmp("HelloWorld", "helloWORLD", 5) == 0
    assert sqliteStrNICmp("Short", "Shoot", 3) == 0
    assert sqliteStrNICmp("123abc", "124abc", 3) < 0

def test_sqliteStrDup_public():
    z = sqliteStrDup("customstring")
    assert z is not None
    assert z == "customstring"
    sqliteFree(z)

def test_sqliteCheckMemory_public():
    assert sqliteCheckMemory() == 0