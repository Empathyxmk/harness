import os
import json

def test_typescript_sources_wordlists_exists():
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_src', '_wordlists.ts'))
    assert os.path.exists(src_path), "_wordlists.ts file is missing"

def test_at_least_one_wordlist_json():
    wordlists_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_src', 'wordlists', 'english.json'))
    assert os.path.exists(wordlists_path), "english.json missing"
    with open(wordlists_path, encoding="utf-8") as wf:
        arr = json.load(wf)
    assert isinstance(arr, list)
    assert len(arr) == 2048