# encoding: utf-8

import os
import sys
import types
import pytest

# Patch sys.path for import of examples if necessary
EXAMPLES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples"))
if EXAMPLES_PATH not in sys.path:
    sys.path.insert(0, EXAMPLES_PATH)

def test_import_examples():
    import collection
    import find_disc
    import releasesearch

def test_run_collection_main(monkeypatch):
    import collection
    if hasattr(collection, "main"):
        # Patch sys.argv for minimal execution
        monkeypatch.setattr("sys.argv", ["collection.py"])
        try:
            collection.main()
        except SystemExit:
            pass  # Allow script-like exit

def test_run_find_disc(monkeypatch):
    import find_disc
    if hasattr(find_disc, "main"):
        monkeypatch.setattr("sys.argv", ["find_disc.py"])
        try:
            find_disc.main()
        except SystemExit:
            pass

def test_run_releasesearch(monkeypatch):
    import releasesearch
    if hasattr(releasesearch, "main"):
        monkeypatch.setattr("sys.argv", ["releasesearch.py"])
        try:
            releasesearch.main()
        except SystemExit:
            pass

# Keep class-based exception definitions on multiple lines to avoid SyntaxError
class DummyRespErr(Exception):
    def __init__(self, cause):
        self.cause = cause

def test_dummy_exception():
    try:
        raise DummyRespErr("something")
    except DummyRespErr as e:
        assert str(e.cause) == "something"