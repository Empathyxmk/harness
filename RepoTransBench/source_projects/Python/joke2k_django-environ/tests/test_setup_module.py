import os
import tempfile
import types
import pytest

import setup as mysetup


def test_read_file_reads_utf8(tmp_path):
    f = tmp_path / "file.txt"
    s = "abc😀"
    f.write_text(s, encoding="utf-8")
    assert mysetup.read_file(str(f)) == s


def test_is_canonical_version():
    # Valid PEP440
    good = [
        '1.0.0',
        '1.2.3',
        '4!1.5.2',
        '2.0.0rc1',
        '1.1.1.post1',
        '1.0.1.dev5',
    ]
    for v in good:
        assert mysetup.is_canonical_version(v)
    # Invalid PEP440
    bad = [
        '1..0',
        'a',
        '..1',
        '1.0b',
        'v.01',
        '1-2-3',
        '-1.0.0'
    ]
    for v in bad:
        assert not mysetup.is_canonical_version(v)


def test_find_meta_success(tmp_path, monkeypatch):
    content = "__version__ = '1.2.3'\n__url__ = 'example.com'\n"
    file = tmp_path / "__init__.py"
    file.write_text(content, encoding="utf-8")
    monkeypatch.setattr(mysetup, "META_CONTENTS", content)
    assert mysetup.find_meta("version") == '1.2.3'
    assert mysetup.find_meta("url") == 'example.com'


def test_find_meta_failure(monkeypatch):
    monkeypatch.setattr(mysetup, "META_CONTENTS", "")
    with pytest.raises(RuntimeError):
        mysetup.find_meta("notfound")


def test_get_version_string_canonical(monkeypatch):
    monkeypatch.setattr(mysetup, "find_meta", lambda m: "1.2.3")
    monkeypatch.setattr(mysetup, "is_canonical_version", lambda v: True)
    assert mysetup.get_version_string() == "1.2.3"


def test_get_version_string_noncanonical(monkeypatch):
    monkeypatch.setattr(mysetup, "find_meta", lambda m: "bad..ver")
    monkeypatch.setattr(mysetup, "is_canonical_version", lambda v: False)
    with pytest.raises(ValueError):
        mysetup.get_version_string()


def test_load_long_description_file_missing(monkeypatch):
    # Simulate missing README.rst and other files
    monkeypatch.setattr(mysetup, "PKG_NAME", "FAKEPKG")
    monkeypatch.setattr(mysetup, "PKG_DIR", "/tmp/none")
    monkeypatch.setattr(mysetup, "META_CONTENTS", "__version__ = '1.0.0'")
    monkeypatch.setattr(mysetup, "find_meta", lambda m: "http://dummy")
    # Remove/patch read_file to raise FileNotFoundError
    def raise_nf(fp):
        raise FileNotFoundError(f"NF: {fp}")
    monkeypatch.setattr(mysetup, "read_file", raise_nf)
    with pytest.raises(RuntimeError):
        mysetup.load_long_description()