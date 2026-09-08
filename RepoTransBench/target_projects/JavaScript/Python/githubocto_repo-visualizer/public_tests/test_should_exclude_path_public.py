import pytest
from unittest.mock import patch, MagicMock
import src.should_exclude_path as sep_module

def test_returns_false_for_empty_path_public():
    assert sep_module.should_exclude_path('', set(), []) is False

def test_returns_true_if_path_in_paths_to_ignore_public():
    assert sep_module.should_exclude_path('alpha', {'alpha'}, []) is True

def test_returns_true_if_micromatch_matches_glob_public():
    with patch("src.should_exclude_path.micromatch_is_match", return_value=True):
        assert sep_module.should_exclude_path('delta', set(), ['delta']) is True

def test_returns_false_if_no_match_public():
    assert sep_module.should_exclude_path('epsilon', {'zeta'}, ['eta']) is False

def test_strips_leading_dot_slash_in_globs_public():
    with patch("src.should_exclude_path.micromatch_is_match", return_value=True):
        assert sep_module.should_exclude_path('./theta', set(), ['theta']) is True

def test_handles_empty_globs_public():
    assert sep_module.should_exclude_path('lambda', set(), ['']) is False