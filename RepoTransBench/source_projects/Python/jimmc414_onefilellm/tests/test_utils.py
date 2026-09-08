import io
import sys
import tempfile
import os
import types
import builtins
import re

import pytest

import utils

def test_safe_file_read_utf8_and_fallback(tmp_path):
    # Write a file with utf-8 encoding
    p = tmp_path / "f.txt"
    data = "Hello äöü"
    p.write_text(data, encoding="utf-8")
    assert utils.safe_file_read(str(p)) == data

    # Write a file with latin1 encoding, fails for utf-8, fallback to latin1
    p2 = tmp_path / "f2.txt"
    text_latin1 = "café"
    p2.write_bytes(text_latin1.encode("latin1"))
    assert utils.safe_file_read(str(p2)) == text_latin1

def test_read_from_clipboard(monkeypatch):
    # Case 1: clipboard with text
    class DummyPyperclip:
        @staticmethod
        def paste():
            return "clipboard content"
    monkeypatch.setattr(utils.pyperclip, "paste", DummyPyperclip.paste)
    assert utils.read_from_clipboard() == "clipboard content"
    # Case 2: clipboard empty string
    monkeypatch.setattr(utils.pyperclip, "paste", lambda : "   ")
    assert utils.read_from_clipboard() is None
    # Case 3: exception occurs
    def raise_exc(): raise utils.pyperclip.PyperclipException("err")
    monkeypatch.setattr(utils.pyperclip, "paste", raise_exc)
    assert utils.read_from_clipboard() is None
    # Try generic Exception:
    def raise_any(): raise Exception("x")
    monkeypatch.setattr(utils.pyperclip, "paste", raise_any)
    assert utils.read_from_clipboard() is None

def test_read_from_stdin(monkeypatch):
    # sys.stdin.isatty = True -> None
    class DummyStdinTTY:
        def isatty(self): return True
    monkeypatch.setattr(sys, "stdin", DummyStdinTTY())
    assert utils.read_from_stdin() is None

    # sys.stdin.isatty = False, stdin has content
    class DummyStdinContent:
        def isatty(self): return False
        def read(self): return "something\n"
    monkeypatch.setattr(sys, "stdin", DummyStdinContent())
    assert utils.read_from_stdin() == "something\n"

    # sys.stdin.isatty = False, stdin empty
    class DummyStdinEmpty:
        def isatty(self): return False
        def read(self): return ""
    monkeypatch.setattr(sys, "stdin", DummyStdinEmpty())
    assert utils.read_from_stdin() is None

    # Exception thrown
    class DummyStdinError:
        def isatty(self): return False
        def read(self): raise Exception("fail")
    monkeypatch.setattr(sys, "stdin", DummyStdinError())
    assert utils.read_from_stdin() is None

@pytest.mark.parametrize("txt,expected", [
    ('{"a": 1}', 'json'),
    ('[1, 2, 3]', 'json'),
    ('a: 3\nb: 4', 'yaml' if utils.yaml else 'text'),
    ('<html>Tag</html>', 'html'),
    ('<!DOCTYPE html>', 'html'),
    ('<div>hello</div>', 'html'),
    ("# Header\nSome text", 'markdown'),
    ("**bold**", 'markdown'),
    ("Just some text", 'text'),
    ("", "text"),
    (" \n\r ", "text"),
])
def test_detect_text_format(txt, expected):
    assert utils.detect_text_format(txt) == expected

def test_parse_as_plaintext_and_markdown():
    # Should return as is
    s = "abc"
    assert utils.parse_as_plaintext(s) == s
    assert utils.parse_as_markdown(s) == s

def test_parse_as_json_and_yaml_and_html():
    s_json = '{"a": 1, "b": 2}'
    parsed = utils.parse_as_json(s_json)
    assert isinstance(parsed, str)
    # YAML (if present)
    if utils.yaml:
        parsed_yaml = utils.parse_as_yaml("k: v\nb: 3")
        assert isinstance(parsed_yaml, str)
    # HTML
    html = "<html><body>Hello</body></html>"
    assert "Hello" in utils.parse_as_html(html)

def test_download_file(tmp_path, monkeypatch):
    # Dummy: Download a small test file using requests
    url = "https://example.com/test.txt"
    dest = tmp_path / "out.txt"
    class DummyResp:
        def __init__(self):
            self.status_code = 200
            self.iter_content_called = False
        def raise_for_status(self):
            assert True
        def iter_content(self, chunk_size): # Simulate yielding some bytes
            self.iter_content_called = True
            yield b'hello'
            yield b'world'
    def dummy_get(*args, **kwargs):
        return DummyResp()
    monkeypatch.setattr(utils.requests, "get", dummy_get)
    utils.download_file(url, str(dest))
    # File should exist and contain 'helloworld'
    assert dest.exists()
    assert dest.read_bytes() == b'helloworld'

def test_is_same_domain():
    # Both on same domain
    assert utils.is_same_domain("https://a.com/page", "https://a.com/x") is True
    # Subdomain different
    assert utils.is_same_domain("https://a.com", "https://sub.a.com/x") is False
    # Ignore scheme
    assert utils.is_same_domain("http://a.com/x", "https://a.com/other") is True

def test_is_within_depth():
    assert utils.is_within_depth("https://a.com", "https://a.com/foo/bar", 2) is True
    assert utils.is_within_depth("https://a.com", "https://a.com/foo/bar/yep", 2) is False
    # ignore scheme
    assert utils.is_within_depth("http://a.com", "https://a.com/f/2", 1) is False

def test_is_excluded_file():
    assert utils.is_excluded_file("/foo/bar/readme.md") is False
    assert utils.is_excluded_file("/foo/dist/file.txt") is True
    assert utils.is_excluded_file("/foo/.git/config") is True

def test_is_allowed_filetype():
    assert utils.is_allowed_filetype("file.py") is True
    assert utils.is_allowed_filetype("file.txt") is True
    assert utils.is_allowed_filetype("file.exe") is False
    assert utils.is_allowed_filetype("file.PY") is True

def test_escape_xml():
    raw = "<a>&b</a>"
    assert utils.escape_xml(raw) == raw

def test_parse_as_yaml_handles_no_yaml(monkeypatch):
    # Simulate utils.yaml = None
    monkeypatch.setattr(utils, "yaml", None)
    assert utils.parse_as_yaml("foo") == "foo"