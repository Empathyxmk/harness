import importlib.util
import os
import pytest

# Try to load ../lib/_wordlists.py or fallback to ../_wordlists.py
def import_wordlists_module_public():
    try:
        mod = importlib.util.spec_from_file_location("_wordlists", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', '_wordlists.py')))
        if mod is not None and mod.loader is not None:
            module = importlib.util.module_from_spec(mod)
            mod.loader.exec_module(module)
            return module
    except Exception:
        pass
    try:
        mod = importlib.util.spec_from_file_location("_wordlists", os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_wordlists.py')))
        if mod is not None and mod.loader is not None:
            module = importlib.util.module_from_spec(mod)
            mod.loader.exec_module(module)
            return module
    except Exception:
        pass
    raise ImportError("Neither lib/_wordlists.py nor _wordlists.py found or importable (public test)")

def get_main_wordlists_obj_public(exported_wordlists):
    if hasattr(exported_wordlists, "wordlists") and isinstance(exported_wordlists.wordlists, dict):
        return exported_wordlists.wordlists
    return exported_wordlists

def test_should_export_known_wordlists_in_public_test():
    alt_expected_keys = [
        'english', 'french', 'italian', 'czech', 'portuguese', 
        'korean', 'japanese', 'chinese_simplified', 'chinese_traditional'
    ]
    try:
        exported_wordlists = import_wordlists_module_public()
    except ImportError:
        pytest.skip("No _wordlists module found (public)")
    main_wordlists_obj = get_main_wordlists_obj_public(exported_wordlists)
    for key in alt_expected_keys:
        assert key in main_wordlists_obj, f"missing key: {key} (public)"
        assert isinstance(main_wordlists_obj[key], list), f"not array: {key} (public)"
        assert len(main_wordlists_obj[key]) > 1000, f"wordlist is too short: {key} ({len(main_wordlists_obj[key])}) (public)"

def test_should_have_unique_lowercase_strings_public():
    alt_expected_keys = [
        'english', 'french', 'italian', 'czech', 'portuguese', 
        'korean', 'japanese', 'chinese_simplified', 'chinese_traditional'
    ]
    try:
        exported_wordlists = import_wordlists_module_public()
    except ImportError:
        pytest.skip("No _wordlists module found (public)")
    main_wordlists_obj = get_main_wordlists_obj_public(exported_wordlists)
    for name in alt_expected_keys:
        wordlist = main_wordlists_obj[name]
        assert isinstance(wordlist, list), f"not array: {name} (public)"
        assert len(set(wordlist)) == len(wordlist), f"Duplicates in {name} (public)"
        for word in wordlist:
            assert isinstance(word, str), f"Non-string in {name} (public)"
            assert word == word.lower(), f"Non-lowercase in {name} (public)"

def test_should_not_contain_spaces_or_empty_items_public():
    alt_expected_keys = [
        'english', 'french', 'italian', 'czech', 'portuguese', 
        'korean', 'japanese', 'chinese_simplified', 'chinese_traditional'
    ]
    try:
        exported_wordlists = import_wordlists_module_public()
    except ImportError:
        pytest.skip("No _wordlists module found (public)")
    main_wordlists_obj = get_main_wordlists_obj_public(exported_wordlists)
    for name in alt_expected_keys:
        wordlist = main_wordlists_obj[name]
        if not isinstance(wordlist, list):
            continue
        for word in wordlist:
            assert not any(c.isspace() for c in word), f"Spaces found in word in {name}: {word} (public)"
            assert len(word) > 0, f"Empty word in {name} (public)"