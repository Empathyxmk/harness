from fourmilab_ent.iso8859 import *

def test_isISOalpha_public():
    assert isISOalpha('B')
    assert isISOalpha('y')
    assert not isISOalpha('2')
    assert not isISOalpha('@')
    assert isISOalpha(0xC4)  # Different Latin-1 uppercase (Ä)
    assert isISOalpha(0xE4)  # Different Latin-1 lowercase (ä)

def test_isISOupper_public():
    assert isISOupper('Z')
    assert not isISOupper('z')
    assert isISOupper(0xD1)  # Latin-1 uppercase (Ñ)

def test_isISOlower_public():
    assert isISOlower('m')
    assert not isISOlower('M')
    assert isISOlower(0xF1)  # Latin-1 lowercase (ñ)

def test_isISOspace_public():
    # Note: isISOspace('\t') was false in original private test, but true in C's isspace.
    # The public C test asserts this is true.
    assert isISOspace('\t')
    assert not isISOspace('B')
    assert isISOspace(0x0A)  # LF is space for some implementations

def test_isISOprint_public():
    assert isISOprint('$')
    assert isISOprint('q')
    assert isISOprint(0xB0)  # Latin-1 printable (°)
    assert not isISOprint('\r')
    assert not isISOprint('\v')