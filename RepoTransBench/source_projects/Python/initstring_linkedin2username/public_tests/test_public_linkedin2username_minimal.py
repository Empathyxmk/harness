import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from linkedin2username import NameMutator

def test_public_import_linkedin2username():
    nm = NameMutator("Lena Horne")
    assert nm is not None

def test_public_main_invocation(monkeypatch):
    import linkedin2username
    import sys

    class DummyArgs:
        company = "dummy"
        format = None
        employees = None
        filter = None
        usernames = False
        csv = False
        limit = None
        pretty = False
    monkeypatch.setattr(sys, "argv", ["linkedin2username", "dummy"])
    # Call main, expecting it to complete without exception
    linkedin2username.main()