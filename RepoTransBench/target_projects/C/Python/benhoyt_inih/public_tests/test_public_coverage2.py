import pytest
from src.inih import ini_parse

def handler_section_key_val_public(user, section, name, value):
    called = user
    if section and name and name == "specialerror":
        return -2
    called[0] += 1
    return 3

def test_public_bad_file():
    try:
        result = ini_parse("tests/notfound_public.ini", None, None)
    except NotImplementedError:
        result = -1
    print(f"test_public_bad_file: {result}")

def test_public_bad_section():
    called = [0]
    try:
        result = ini_parse("tests/bad_multi.ini", handler_section_key_val_public, called)
    except NotImplementedError:
        result = 0
    print(f"test_public_bad_section: {result}, called={called[0]}")

def test_public_bad_comment():
    called = [0]
    try:
        result = ini_parse("tests/bad_comment.ini", handler_section_key_val_public, called)
    except NotImplementedError:
        result = 0
    print(f"test_public_bad_comment: {result}, called={called[0]}")

def test_public_long_section():
    called = [0]
    try:
        result = ini_parse("tests/long_section.ini", handler_section_key_val_public, called)
    except NotImplementedError:
        result = 0
    print(f"test_public_long_section: {result}, called={called[0]}")

def test_public_bom():
    called = [0]
    try:
        result = ini_parse("tests/bom.ini", handler_section_key_val_public, called)
    except NotImplementedError:
        result = 0
    print(f"test_public_bom: {result}, called={called[0]}")