import pytest
import stat
from unittest.mock import MagicMock

import src.process_dir as process_dir_module
import src.should_exclude_path as should_exclude_path_module

def make_stat_mock(is_dir, size):
    import types
    st_mode = stat.S_IFDIR if is_dir else stat.S_IFREG
    mock = types.SimpleNamespace()
    mock.st_mode = st_mode
    mock.st_size = size
    return mock

def test_skips_excluded_files(monkeypatch):
    readdir_mock = MagicMock(return_value=['foo'])
    stat_mock = MagicMock(side_effect=[make_stat_mock(True, 1)])
    should_exclude_mock = MagicMock(side_effect=lambda abs_path, name: name == 'foo')
    monkeypatch.setattr("os.listdir", readdir_mock)
    monkeypatch.setattr("os.stat", stat_mock)
    monkeypatch.setattr(process_dir_module, "should_exclude_path", should_exclude_mock)

    tree = process_dir_module.process_dir('testdir', [], [])
    assert tree["name"] == "testdir"
    assert "children" in tree
    assert tree["children"] == []

def test_recurses_directories_and_files(monkeypatch):
    readdir_mock = MagicMock(side_effect=[['file1', 'dir2'], []])
    stat_mock = MagicMock(side_effect=[
        make_stat_mock(True, 100),    # root
        make_stat_mock(False, 10),    # file1
        make_stat_mock(True, 90),     # dir2
    ])
    should_exclude_mock = MagicMock(return_value=False)
    monkeypatch.setattr("os.listdir", readdir_mock)
    monkeypatch.setattr("os.stat", stat_mock)
    monkeypatch.setattr(process_dir_module, "should_exclude_path", should_exclude_mock)

    tree = process_dir_module.process_dir('/root', [], [])
    assert len(tree["children"]) == 2
    assert tree["children"][0]["name"] == 'file1'
    assert tree["children"][1]["name"] == 'dir2'
    assert tree["children"][1]["children"] == []

def test_returns_null_on_stat_error(monkeypatch):
    stat_mock = MagicMock(side_effect=OSError("fail"))
    monkeypatch.setattr("os.stat", stat_mock)
    result = process_dir_module.process_dir('/bad', [], [])
    assert result is None

def test_handles_empty_directories(monkeypatch):
    stat_mock = MagicMock(return_value=make_stat_mock(True, 42))
    readdir_mock = MagicMock(return_value=[])
    should_exclude_mock = MagicMock(return_value=False)
    monkeypatch.setattr("os.stat", stat_mock)
    monkeypatch.setattr("os.listdir", readdir_mock)
    monkeypatch.setattr(process_dir_module, "should_exclude_path", should_exclude_mock)

    tree = process_dir_module.process_dir('/emptydir', [], [])
    assert tree["children"] == []
    assert tree["name"] == "emptydir"
    assert tree["size"] == 42

def test_handles_regular_files(monkeypatch):
    stat_mock = MagicMock(return_value=make_stat_mock(False, 8))
    monkeypatch.setattr("os.stat", stat_mock)
    tree = process_dir_module.process_dir('/file', [], [])
    assert tree["name"] == "file"
    assert tree["size"] == 8
    assert "children" not in tree