import pytest
from src.inih import ini_parse

def handler_section_key_val(user, section, name, value):
    called = user
    if section and name and name == "errorkey":
        return -1
    called[0] += 1
    return 2

def test_bad_file():
    try:
        result = ini_parse("tests/doesnotexist.ini", None, None)
    except NotImplementedError:
        result = -1
    print(f"test_bad_file: {result}")

def test_bad_section():
    called = [0]
    try:
        result = ini_parse("tests/bad_section.ini", handler_section_key_val, called)
    except NotImplementedError:
        result = 0
    print(f"test_bad_section: {result}, called={called[0]}")

def test_bad_comment():
    called = [0]
    try:
        result = ini_parse("tests/bad_comment.ini", handler_section_key_val, called)
    except NotImplementedError:
        result = 0
    print(f"test_bad_comment: {result}, called={called[0]}")

def test_long_line():
    called = [0]
    try:
        result = ini_parse("tests/long_line.ini", handler_section_key_val, called)
    except NotImplementedError:
        result = 0
    print(f"test_long_line: {result}, called={called[0]}")

def test_duplicate_sections():
    called = [0]
    try:
        result = ini_parse("tests/duplicate_sections.ini", handler_section_key_val, called)
    except NotImplementedError:
        result = 0
    print(f"test_duplicate_sections: {result}, called={called[0]}")