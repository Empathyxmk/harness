import io
import sys
import tempfile
import os
import types
import builtins
import re

import pytest

import utils

def test_safe_file_read_utf8_and_fallback_public(tmp_path):
    # Write a file with utf-8 encoding (different data)
    p = tmp_path / "foo.txt"
    data = "Testing äßü"
    p.write_text(data, encoding="utf-8")
    assert utils.safe_file_read(str(p)) == data

    # Write a file with latin1 encoding, fails for utf-8, fallback to latin1 (different text)
    p2 = tmp_path / "bar.txt"
    text_latin1 = "niño"
    p2.write_bytes(text_latin1.encode("latin1"))
    assert utils.safe_file_read(str(p2)) == text_latin1

def test_read_from_clipboard_public(monkeypatch):
    # Case 1: clipboard with text (different content)
    class DummyPyperclip:
        @staticmethod
        def paste():
            return "public clipboard"
    monkeypatch.setattr(utils.pyperclip, "paste", DummyPyperclip.paste)
    assert utils.read_from_clipboard() == "public clipboard"
    # Case 2: clipboard empty string
    monkeypatch.setattr(utils.pyperclip, "paste", lambda : "    ")
    assert utils.read_from_clipboard() is None
    # Case 3: exception occurs
    def raise_exc(): raise utils.pyperclip.PyperclipException("fail")
    monkeypatch.setattr(utils.pyperclip, "paste", raise_exc)
    assert utils.read_from_clipboard() is None
    # Try generic Exception:
    def raise_any(): raise Exception("error")
    monkeypatch.setattr(utils.pyperclip, "paste", raise_any)
    assert utils.read_from_clipboard() is None

def test_read_from_stdin_public(monkeypatch):
    # sys.stdin.isatty = True -> None
    class DummyStdinTTY:
        def isatty(self): return True
    monkeypatch.setattr(sys, "stdin", DummyStdinTTY())
    assert utils.read_from_stdin() is None

    # sys.stdin.isatty = False, stdin has content (different string)
    class DummyStdinContent:
        def isatty(self): return False
        def read(self): return "different input\n"
    monkeypatch.setattr(sys, "stdin", DummyStdinContent())
    assert utils.read_from_stdin() == "different input\n"

    # sys.stdin.isatty = False, stdin empty
    class DummyStdinEmpty:
        def isatty(self): return False
        def read(self): return ""
    monkeypatch.setattr(sys, "stdin", DummyStdinEmpty())
    assert utils.read_from_stdin() is None

    # Exception thrown
    class DummyStdinError:
        def isatty(self): return False
        def read(self): raise Exception("fail-public")
    monkeypatch.setattr(sys, "stdin", DummyStdinError())
    assert utils.read_from_stdin() is None

@pytest.mark.parametrize("txt,expected", [
    ('{"foo": 42}', 'json'),
    ('[100, 200, 300]', 'json'),
    ('x: 7\ny: 8', 'yaml' if utils.yaml else 'text'),
    ('<HTML>Tag</HTML>', 'html'),
    ('<!DOCTYPE HTML>', 'html'),
    ('<span>public</span>', 'html'),
    ("## Subheader\nSome text", 'markdown'),
    ("*item*", 'markdown'),
    ("A random sentence", 'text'),
    (" ", "text"),
    ("\n\n", "text"),
])
def test_detect_text_format_public(txt, expected):
    assert utils.detect_text_format(txt) == expected

def test_parse_as_plaintext_and_markdown_public():
    # Should return as is (different string)
    s = "xyz"
    assert utils.parse_as_plaintext(s) == s
    assert utils.parse_as_markdown(s) == s

def test_parse_as_json_and_yaml_and_html_public():
    s_json = '{"x": 99, "y": 88}'
    parsed = utils.parse_as_json(s_json)
    assert isinstance(parsed, str)
    # YAML (if present)
    if utils.yaml:
        parsed_yaml = utils.parse_as_yaml("foo: bar\nbaz: quux")
        assert isinstance(parsed_yaml, str)
    # HTML (different content)
    html = "<html><body>World</body></html>"
    assert "World" in utils.parse_as_html(html)

def test_download_file_public(tmp_path, monkeypatch):
    # Dummy: Download a small test file using requests (different content)
    url = "https://example.com/some.txt"
    dest = tmp_path / "some_output.txt"
    class DummyResp:
        def __init__(self):
            self.status_code = 200
            self.iter_content_called = False
        def raise_for_status(self):
            pass
        def iter_content(self, chunk_size): # Simulate yielding some bytes
            self.iter_content_called = True
            yield b'foo'
            yield b'bar'
    def dummy_get(*args, **kwargs):
        return DummyResp()
    monkeypatch.setattr(utils.requests, "get", dummy_get)
    utils.download_file(url, str(dest))
    # File should exist and contain 'foobar'
    assert dest.exists()
    assert dest.read_bytes() == b'foobar'

def test_is_same_domain_public():
    # Both on same domain (different domains used)
    assert utils.is_same_domain("https://b.com/page", "https://b.com/y") is True
    # Subdomain different
    assert utils.is_same_domain("https://b.com", "https://sub.b.com/a") is False
    # Ignore scheme
    assert utils.is_same_domain("http://b.com/xy", "https://b.com/zzz") is True

def test_is_within_depth_public():
    assert utils.is_within_depth("https://b.com", "https://b.com/abc/def", 2) is True
    assert utils.is_within_depth("https://b.com", "https://b.com/a/b/c/d", 3) is False
    # ignore scheme
    assert utils.is_within_depth("http://b.com", "https://b.com/a/b", 1) is False

def test_is_excluded_file_public():
    assert utils.is_excluded_file("/bar/src/main.py") is False
    assert utils.is_excluded_file("/bar/node_modules/script.js") is True
    assert utils.is_excluded_file("/bar/.git/description") is True

def test_is_allowed_filetype_public():
    assert utils.is_allowed_filetype("main.go") is True
    assert utils.is_allowed_filetype("foo.md") is True
    assert utils.is_allowed_filetype("file.dll") is False
    assert utils.is_allowed_filetype("file.MD") is True

def test_escape_xml_public():
    raw = "<public>&amp;</public>"
    assert utils.escape_xml(raw) == raw

def test_parse_as_yaml_handles_no_yaml_public(monkeypatch):
    # Simulate utils.yaml = None, different text
    monkeypatch.setattr(utils, "yaml", None)
    assert utils.parse_as_yaml("bar") == "bar"