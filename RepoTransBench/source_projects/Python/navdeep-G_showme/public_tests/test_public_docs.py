import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import showme

def test_public_docs():
    # Slightly different docstring test
    from showme import core
    doc = core.__doc__
    assert isinstance(doc, str)
    assert "showme" in doc.lower() or "core" in doc.lower()