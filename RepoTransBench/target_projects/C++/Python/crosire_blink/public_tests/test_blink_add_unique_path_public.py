import pytest

def add_unique_path(paths, new_path):
    if new_path not in paths:
        paths.append(new_path)

def test_blink_add_unique_path_public_insert_completely_new_path():
    paths = ["alpha/fileA", "bravo/fileB"]
    add_unique_path(paths, "charlie/fileC")
    assert len(paths) == 3
    assert paths[-1] == "charlie/fileC"

def test_blink_add_unique_path_public_insert_existing_path_public():
    paths = ["test/foo", "test/bar"]
    add_unique_path(paths, "test/bar")  # Duplicate
    assert len(paths) == 2
    assert paths[0] == "test/foo"
    assert paths[1] == "test/bar"

def test_blink_add_unique_path_public_insert_similar_but_distinct():
    paths = ["myfolder/log.txt"]
    add_unique_path(paths, "myfolder/log.txt.bak")
    assert len(paths) == 2
    assert paths[1] == "myfolder/log.txt.bak"