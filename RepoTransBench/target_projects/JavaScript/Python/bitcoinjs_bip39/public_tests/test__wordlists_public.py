import os
import json

def test_typescript_sources_wordlists_exists_public():
    alt_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_src', '_wordlists.ts'))
    assert os.path.exists(alt_src_path), "_wordlists.ts file is missing (public)"

def test_at_least_one_non_english_wordlist_json_public():
    alt_wordlists_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_src', 'wordlists', 'french.json'))
    assert os.path.exists(alt_wordlists_path)
    with open(alt_wordlists_path, encoding="utf-8") as wf:
        arr = json.load(wf)
    assert isinstance(arr, list)
    assert len(arr) == 2048