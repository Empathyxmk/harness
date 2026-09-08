from src.codeblocks import util

def test_cloneObj_clones_plain_objects_public():
    a = {'foo': {'bar': [3, 4]}}
    b = util.cloneObj(a)
    assert b is not a
    assert b == a
    b['foo']['bar'].append(5)
    assert a['foo']['bar'] != b['foo']['bar']

def test_cloneObj_returns_argument_if_not_object_public():
    assert util.cloneObj(None) is None
    assert util.cloneObj('test') == 'test'

def test_getUserPrefs_returns_correct_public():
    assert util.getUserPrefs() == {'language': 'js', 'theme': 'dark', 'noBackground': True}

def test_alreadySaved_true_if_match_public():
    prefs = {'language': 'js', 'theme': 'dark', 'noBackground': True}
    assert util.alreadySaved(prefs) is True

def test_alreadySaved_false_if_not_match_public():
    prefs = {'language': 'py', 'theme': 'light', 'noBackground': True}
    assert util.alreadySaved(prefs) is False

def test_cacheSelection_alreadySelected_public():
    # Reset the cache for isolation
    util._reset_selection_cache()
    assert util.cacheSelection('different') is True
    assert util.alreadySelected('zzz') is False
    assert util.alreadySelected('different') is True

def test_loadThemes_public():
    assert util.loadThemes({'something': 'else'}) == ['base-theme']

def test_getThemeCssFromCache_public():
    assert util.getThemeCssFromCache({'a': 1}, 'base-theme') is None
    assert util.getThemeCssFromCache({'b': 2}, 'other') == 'css2'