NONE = 0
READ = 1
WRITE = 2
EXECUTE = 4

def has_read(prot):
    return (prot & READ) != 0

def has_write(prot):
    return (prot & WRITE) != 0

def has_execute(prot):
    return (prot & EXECUTE) != 0

def set_prot(initial, to_set):
    return initial | to_set

def clear_prot(initial, to_clear):
    return initial & ~to_clear

def test_protection_public():
    prot = NONE
    # Change order, combine tests, and use different order to test logic with the same functions.
    prot = set_prot(prot, WRITE)
    assert not has_read(prot)
    assert has_write(prot)
    assert not has_execute(prot)

    prot = set_prot(prot, EXECUTE)
    assert has_execute(prot)
    assert has_write(prot)
    assert not has_read(prot)

    prot = set_prot(prot, READ)
    assert has_read(prot)
    assert has_execute(prot)
    assert has_write(prot)

    prot = clear_prot(prot, WRITE)
    assert not has_write(prot)
    assert has_read(prot)
    assert has_execute(prot)

    prot = clear_prot(prot, NONE) # clearing NONE should not change
    assert has_read(prot)
    assert has_execute(prot)

    prot = clear_prot(prot, EXECUTE)
    assert not has_execute(prot)
    assert has_read(prot)

    prot = clear_prot(prot, READ)
    assert not has_read(prot)