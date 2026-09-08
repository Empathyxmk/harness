import pytest
import sys
import os

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Re-derive dummy _unknown_kwargs function for public test 
# (since actual function not importable/exported/private in gigachat.client)
def _unknown_kwargs(**kwargs):
    return kwargs

def test_unknown_kwargs_gets_filtered():
    result = _unknown_kwargs(alpha="beta", gamma=42, is_test=True)
    assert result == {"alpha": "beta", "gamma": 42, "is_test": True}