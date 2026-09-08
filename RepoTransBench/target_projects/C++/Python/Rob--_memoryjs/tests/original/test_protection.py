def has_read(prot):
    return (prot & 1) != 0

def has_write(prot):
    return (prot & 2) != 0

def has_execute(prot):
    return (prot & 4) != 0

def set_prot(initial, to_set):
    return initial | to_set

def clear_prot(initial, to_clear):
    return initial & ~to_clear

NONE = 0
READ = 1
WRITE = 2
EXECUTE = 4

def test_protection_scenarios():
    prot = NONE
    prot = set_prot(prot, READ)
    assert has_read(prot)
    assert not has_write(prot)
    assert not has_execute(prot)

    prot = set_prot(prot, WRITE)
    assert has_write(prot)

    prot = set_prot(prot, EXECUTE)
    assert has_execute(prot)

    prot = clear_prot(prot, READ)
    assert not has_read(prot)
    prot = clear_prot(prot, WRITE)
    assert not has_write(prot)
    prot = clear_prot(prot, EXECUTE)
    assert not has_execute(prot)