import importlib.util
import os

# Try to load ../lib/_wordlists.js or fallback to ../_wordlists.js
def import_wordlists_module():
    try:
        # Try the compiled location
        mod = importlib.util.spec_from_file_location("_wordlists", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', '_wordlists.py')))
        if mod is not None and mod.loader is not None:
            module = importlib.util.module_from_spec(mod)
            mod.loader.exec_module(module)
            return module
    except Exception:
        pass
    # Fallback to root
    try:
        mod = importlib.util.spec_from_file_location("_wordlists", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_wordlists.py')))
        if mod is not None and mod.loader is not None:
            module = importlib.util.module_from_spec(mod)
            mod.loader.exec_module(module)
            return module
    except Exception:
        pass
    raise ImportError("Neither lib/_wordlists.py nor _wordlists.py found or importable")

import pytest

def get_main_wordlists_obj(exported_wordlists):
    # If a wrapping "wordlists" object, use that. Otherwise, use the main export.
    if hasattr(exported_wordlists, "wordlists") and isinstance(exported_wordlists.wordlists, dict):
        return exported_wordlists.wordlists
    return exported_wordlists

def test_should_export_all_expected_wordlists():
    expected_keys = [
        'english', 'japanese', 'chinese_simplified', 'chinese_traditional',
        'french', 'italian', 'spanish', 'czech', 'korean', 'portuguese']
    try:
        exported_wordlists = import_wordlists_module()
    except ImportError:
        pytest.skip("No _wordlists module found")
    main_wordlists_obj = get_main_wordlists_obj(exported_wordlists)
    for key in expected_keys:
        assert key in main_wordlists_obj, f"missing key: {key}"
        assert isinstance(main_wordlists_obj[key], list), f"not array: {key}"
        assert len(main_wordlists_obj[key]) > 1000, f"wordlist is too short: {key} ({len(main_wordlists_obj[key])})"

def test_should_have_all_wordlists_unique_lowercase():
    expected_keys = [
        'english', 'japanese', 'chinese_simplified', 'chinese_traditional',
        'french', 'italian', 'spanish', 'czech', 'korean', 'portuguese']
    try:
        exported_wordlists = import_wordlists_module()
    except ImportError:
        pytest.skip("No _wordlists module found")
    main_wordlists_obj = get_main_wordlists_obj(exported_wordlists)
    for name in expected_keys:
        wordlist = main_wordlists_obj[name]
        assert isinstance(wordlist, list), f"not array: {name}"
        assert len(set(wordlist)) == len(wordlist), f"Duplicates in {name}"
        for word in wordlist:
            assert isinstance(word, str), f"Non-string in {name}"
            assert word == word.lower(), f"Non-lowercase in {name}"

def test_should_not_contain_obvious_garbage():
    expected_keys = [
        'english', 'japanese', 'chinese_simplified', 'chinese_traditional',
        'french', 'italian', 'spanish', 'czech', 'korean', 'portuguese']
    try:
        exported_wordlists = import_wordlists_module()
    except ImportError:
        pytest.skip("No _wordlists module found")
    main_wordlists_obj = get_main_wordlists_obj(exported_wordlists)
    for name in expected_keys:
        wordlist = main_wordlists_obj[name]
        if not isinstance(wordlist, list):
            continue
        for word in wordlist:
            assert not any(c.isspace() for c in word), f"Spaces found in word in {name}: {word}"
            assert len(word) > 0, f"Empty word in {name}"