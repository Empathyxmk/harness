import pytest

def file_desc(name):
    return f"PUBLIC: {name}"

def test_file_desc_output_public():
    assert file_desc("foo") == "PUBLIC: foo"
    assert file_desc("42.txt") == "PUBLIC: 42.txt"

def test_file_desc_output_unicode():
    assert file_desc("日本語") == "PUBLIC: 日本語"