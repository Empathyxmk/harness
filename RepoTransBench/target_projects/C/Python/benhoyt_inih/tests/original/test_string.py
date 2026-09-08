import pytest
from src.inih import ini_parse_string

User = [None]
Prev_section = [""]

def dumper(user, section, name, value):
    User[0] = user
    if section != Prev_section[0]:
        print(f"... [{section}]")
        Prev_section[0] = section
    print(f"... {name}={value};")
    return 1

def parse(name, string):
    u = [100]
    Prev_section[0] = ""
    try:
        e = ini_parse_string(string, dumper, u[0])
    except NotImplementedError:
        e = 0
    print(f"{name}: e={e} user={u[0]}")
    u[0] += 1

def test_string_cases():
    parse("empty string", "")
    parse("basic", "[section]\nfoo = bar\nbazz = buzz quxx")
    parse("crlf", "[section]\r\nhello = world\r\nforty_two = 42\r\n")
    parse("long line", "[sec]\nfoo = 01234567890123456789\nbar=4321\n")
    parse("long continued", "[sec]\nfoo = 0123456789012bix=1234\n")
    parse("error", "[s]\na=1\nb\nc=3")