import pytest
from src.codeblocks import util

def test_cloneObj_clones_plain_objects():
    a = {'x': {'y': [1,2]}}
    b = util.cloneObj(a)
    assert b is not a
    assert b == a
    b['x']['y'].append(3)
    assert a['x']['y'] != b['x']['y']

def test_cloneObj_returns_argument_if_not_object():
    assert util.cloneObj(None) is None
    assert util.cloneObj(1) == 1

def test_getUserPrefs_returns_correct():
    assert util.getUserPrefs() == {'language': 'js', 'theme': 'dark', 'noBackground': True}

def test_alreadySaved_true_if_match():
    prefs = {'language': 'js', 'theme': 'dark', 'noBackground': True}
    assert util.alreadySaved(prefs) is True

def test_alreadySaved_false_if_not_match():
    prefs = {'language': 'js', 'theme': 'light', 'noBackground': False}
    assert util.alreadySaved(prefs) is False

def test_cacheSelection_alreadySelected():
    # Reset the cache for isolation
    util._reset_selection_cache()
    assert util.cacheSelection('test') is True
    assert util.alreadySelected('abc') is False
    assert util.alreadySelected('test') is True

def test_loadThemes():
    assert util.loadThemes({}) == ['base-theme']

def test_getThemeCssFromCache():
    assert util.getThemeCssFromCache({}, 'base-theme') is None
    assert util.getThemeCssFromCache({}, 'other') == 'css2'