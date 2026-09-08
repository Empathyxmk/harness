from fourmilab_ent.iso8859 import *

def test_isISOalpha():
    assert isISOalpha('A')
    assert isISOalpha('z')
    assert not isISOalpha('1')
    assert not isISOalpha('!')
    assert isISOalpha(0xC1)  # Latin-1 upper
    assert isISOalpha(0xDF)  # Latin-1 lower (ß)

def test_isISOupper():
    assert isISOupper('A')
    assert not isISOupper('a')
    assert isISOupper(0xC1)  # Latin-1 upper

def test_isISOlower():
    assert isISOlower('a')
    assert not isISOlower('A')
    assert isISOlower(0xDF)  # Latin-1 lower

def test_isISOspace():
    assert isISOspace(' ')
    assert not isISOspace('A')
    assert isISOspace(0xA0)

def test_isISOprint():
    assert isISOprint('!')
    assert isISOprint('Z')
    assert isISOprint(0xA0)
    assert not isISOprint('\n')
    assert not isISOprint('\t') # Note: isspace('\t') is true, but isprint is not

def test_toISOupper():
    assert toISOupper('a') == ord('A')
    assert toISOupper('A') == ord('A')
    assert toISOupper(0xE1) == 0xC1  # Latin-1: á (0xE1) to Á (0xC1)

def test_toISOlower():
    assert toISOlower('A') == ord('a')
    assert toISOlower('a') == ord('a')
    assert toISOlower(0xC1) == 0xE1  # Latin-1: Á (0xC1) to á (0xE1)