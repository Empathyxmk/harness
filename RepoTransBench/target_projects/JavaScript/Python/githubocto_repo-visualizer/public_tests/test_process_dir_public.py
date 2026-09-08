import pytest
import stat
from unittest.mock import MagicMock

import src.process_dir as process_dir_module

def make_stat_mock(is_dir, size):
    import types
    st_mode = stat.S_IFDIR if is_dir else stat.S_IFREG
    mock = types.SimpleNamespace()
    mock.st_mode = st_mode
    mock.st_size = size
    return mock

def test_skips_excluded_files_public(monkeypatch):
    readdir_mock = MagicMock(return_value=['bar'])
    stat_mock = MagicMock(side_effect=[make_stat_mock(True, 2)])
    should_exclude_mock = MagicMock(side_effect=lambda abs_path, name: name == 'bar')
    monkeypatch.setattr("os.listdir", readdir_mock)
    monkeypatch.setattr("os.stat", stat_mock)
    monkeypatch.setattr(process_dir_module, "should_exclude_path", should_exclude_mock)

    tree = process_dir_module.process_dir('pubdir', [], [])
    assert tree["name"] == 'pubdir'
    assert "children" in tree
    assert tree["children"] == []

def test_recurses_directories_and_files_public(monkeypatch):
    readdir_mock = MagicMock(side_effect=[['x.txt', 'data'], ['deep.txt']])
    stat_mock = MagicMock(side_effect=[
        make_stat_mock(True, 222),    # root
        make_stat_mock(False, 11),    # x.txt
        make_stat_mock(True, 211),    # data
        make_stat_mock(False, 33),    # deep.txt
    ])
    should_exclude_mock = MagicMock(return_value=False)
    monkeypatch.setattr("os.listdir", readdir_mock)
    monkeypatch.setattr("os.stat", stat_mock)
    monkeypatch.setattr(process_dir_module, "should_exclude_path", should_exclude_mock)

    tree = process_dir_module.process_dir('/public_root', [], [])
    assert len(tree["children"]) == 2
    assert tree["children"][0]["name"] == 'x.txt'
    assert tree["children"][1]["name"] == 'data'
    assert tree["children"][1]["children"][0]["name"] == 'deep.txt'

def test_returns_null_on_stat_error_public(monkeypatch):
    stat_mock = MagicMock(side_effect=OSError("public fail"))
    monkeypatch.setattr("os.stat", stat_mock)
    result = process_dir_module.process_dir('/faildir', [], [])
    assert result is None

def test_handles_empty_directories_public(monkeypatch):
    stat_mock = MagicMock(return_value=make_stat_mock(True, 123))
    readdir_mock = MagicMock(return_value=[])
    should_exclude_mock = MagicMock(return_value=False)
    monkeypatch.setattr("os.stat", stat_mock)
    monkeypatch.setattr("os.listdir", readdir_mock)
    monkeypatch.setattr(process_dir_module, "should_exclude_path", should_exclude_mock)

    tree = process_dir_module.process_dir('/public_empty', [], [])
    assert tree["children"] == []
    assert tree["name"] == 'public_empty'
    assert tree["size"] == 123

def test_handles_regular_files_public(monkeypatch):
    stat_mock = MagicMock(return_value=make_stat_mock(False, 6))
    monkeypatch.setattr("os.stat", stat_mock)
    tree = process_dir_module.process_dir('/myfile', [], [])
    assert tree["name"] == "myfile"
    assert tree["size"] == 6
    assert "children" not in tree