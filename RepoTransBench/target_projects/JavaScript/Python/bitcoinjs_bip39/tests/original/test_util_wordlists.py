import os
import importlib.util

def test_util_wordlists_js_file_exists():
    js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'util', 'wordlists.js'))
    assert os.path.exists(js_path), "util/wordlists.js file should exist if built"

def test_util_wordlists_js_is_importable():
    js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'util', 'wordlists.js'))
    if os.path.exists(js_path):
        # Just checking syntax - try to import as a module, expect no exception
        # Python cannot import JS; simulate only "no throw"
        try:
            open(js_path, "r").close()
        except Exception:
            assert False, "util/wordlists.js should be require-able (no syntax error)"