import pytest
from src.inih import ini_parse

User = [None]
Prev_section = [""]

def dumper(user, section, name, value):
    User[0] = user
    if (not name) or (section != Prev_section[0]):
        print(f"... [{section}]")
        Prev_section[0] = section
    if not name:
        return 1
    print(f"... {name}{'='+value if value else ''};")
    if not value:
        return 1
    if name == "user" and value == "parse_error":
        return 0
    return 1

def parse(fname):
    u = [100]
    Prev_section[0] = ""
    try:
        e = ini_parse(fname, dumper, u[0])
    except NotImplementedError:
        e = 0
    print(f"{fname}: e={e} user={u[0]}")
    u[0] += 1

def test_all_files():
    parse("no_file.ini")
    parse("normal.ini")
    parse("bad_section.ini")
    parse("bad_comment.ini")
    parse("user_error.ini")
    parse("multi_line.ini")
    parse("bad_multi.ini")
    parse("bom.ini")
    parse("duplicate_sections.ini")
    parse("no_value.ini")
    parse("long_section.ini")
    parse("long_line.ini")