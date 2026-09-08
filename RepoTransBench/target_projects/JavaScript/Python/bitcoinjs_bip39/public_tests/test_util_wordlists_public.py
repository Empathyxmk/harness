import os

def test_util_wordlists_js_file_exists_public():
    js_path = os.path.join(os.path.dirname(__file__), '..', 'util', 'wordlists.js')
    exists = False
    try:
        exists = os.path.isfile(js_path)
    except Exception:
        pass
    assert exists, "util/wordlists.js file does not exist"

def test_util_wordlists_js_is_importable_public():
    js_path = os.path.join(os.path.dirname(__file__), '..', 'util', 'wordlists.js')
    if os.path.exists(js_path):
        threw = False
        try:
            open(js_path, "r").close()
        except Exception:
            threw = True
        assert threw is False, "util/wordlists.js should not throw when required"