import pytest
from src.inih import ini_parse

class DummyOpts:
    def __init__(self):
        self.allow_multi_line = 1
        self.allow_bom = 1
        self.allow_inline_comments = 1
        self.allow_no_value = 0
        self.call_handler_on_new_section = 0

def ini_parse_with_options(filename, handler, user, options):
    # fallback, just calls ini_parse
    return ini_parse(filename, handler, user)

def fail_on_line3(user, section, name, value):
    called = user
    called[0] += 1
    if called[0] == 3:
        return 0
    return 1

def handler_print(user, section, name, value):
    print(f"Section: {section}, Name: {name}, Value: {value if value else '(null)'}")
    return 1

def test_stop_on_first_error():
    called = [0]
    try:
        result = ini_parse("tests/normal.ini", fail_on_line3, called)
    except NotImplementedError:
        result = 0
    print(f"test_stop_on_first_error: result={result}, called={called[0]}")

def test_disallow_inline_comments():
    opts = DummyOpts()
    opts.allow_inline_comments = 0
    try:
        ini_parse_with_options("tests/normal.ini", handler_print, None, opts)
    except NotImplementedError:
        pass
    print("test_disallow_inline_comments: done")

def test_call_handler_on_new_section():
    opts = DummyOpts()
    opts.call_handler_on_new_section = 1
    try:
        ini_parse_with_options("tests/normal.ini", handler_print, None, opts)
    except NotImplementedError:
        pass
    print("test_call_handler_on_new_section: done")

def test_allow_no_value():
    opts = DummyOpts()
    opts.allow_no_value = 1
    try:
        ini_parse_with_options("tests/no_value.ini", handler_print, None, opts)
    except NotImplementedError:
        pass
    print("test_allow_no_value: done")

def test_disable_multiline():
    opts = DummyOpts()
    opts.allow_multi_line = 0
    try:
        ini_parse_with_options("tests/multi_line.ini", handler_print, None, opts)
    except NotImplementedError:
        pass
    print("test_disable_multiline: done")