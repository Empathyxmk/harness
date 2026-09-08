import pytest
from src.inih import ini_parse_string

PubUser = [None]
Prev_section_public = [""]

def dumper_public(user, section, name, value):
    PubUser[0] = user
    if section != Prev_section_public[0]:
        print(f"[pubs] ... [{section}]")
        Prev_section_public[0] = section
    print(f"[pubs] ... {name}={value};")
    return 1

def parse_public(name, string):
    u = [200]
    Prev_section_public[0] = ""
    try:
        e = ini_parse_string(string, dumper_public, u[0])
    except NotImplementedError:
        e = 0
    print(f"{name}: e={e} user={u[0]}")
    u[0] += 1

def test_public_string_cases():
    parse_public("pub_empty string", "")
    parse_public("pub_simple", "[alpha]\nkey1 = foo\nkey2 = bar baz")
    parse_public("pub_cr", "[beta]\rkeyA = world\rkeyB = 24\r")
    parse_public("pub_publine", "[mine]\nx = abcdefghijklmnopqrst\nb=1234\n")
    parse_public("pub_error2", "[p]\ny=2\nq\nz=9")