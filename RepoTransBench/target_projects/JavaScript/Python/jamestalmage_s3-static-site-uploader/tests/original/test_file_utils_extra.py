import pytest

def make_file_dict(name):
    return {"name": name, "content": f"File: {name}"}

def file_length(file_dict):
    return len(file_dict["content"])

def test_make_file_dict_and_length():
    f = make_file_dict("abc.txt")
    assert f["name"] == "abc.txt"
    assert f["content"] == "File: abc.txt"
    assert file_length(f) == len("File: abc.txt")

def test_file_length_empty_file():
    f = {"name": "empty", "content": ""}
    assert file_length(f) == 0

def test_file_length_nonascii():
    f = {"name": "日本語", "content": "こんにちは"}
    assert file_length(f) == 5