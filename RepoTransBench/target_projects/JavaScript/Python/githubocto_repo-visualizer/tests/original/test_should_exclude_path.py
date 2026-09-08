import pytest
from unittest.mock import patch, MagicMock
import src.should_exclude_path as sep_module

def test_returns_false_for_empty_path():
    assert sep_module.should_exclude_path('', set(), []) is False

def test_returns_true_if_path_in_paths_to_ignore():
    assert sep_module.should_exclude_path('foo', {'foo'}, []) is True

def test_returns_true_if_micromatch_matches_glob(monkeypatch):
    with patch("src.should_exclude_path.micromatch_is_match", return_value=True):
        assert sep_module.should_exclude_path('bar', set(), ['bar']) is True

def test_returns_false_if_no_match():
    assert sep_module.should_exclude_path('baz', {'xxx'}, ['no']) is False

def test_strips_leading_dot_slash_in_globs(monkeypatch):
    with patch("src.should_exclude_path.micromatch_is_match", return_value=True):
        assert sep_module.should_exclude_path('./baz', set(), ['baz']) is True

def test_handles_empty_globs():
    assert sep_module.should_exclude_path('baz', set(), ['']) is False