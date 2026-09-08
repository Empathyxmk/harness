import sys
import os
import pytest

# Ensure src directory is on PYTHONPATH for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from zapv2 import core

def test_client_title_new_case():
    # Testing title returns a string and is not empty - using a different check
    title = core.title()
    assert isinstance(title, str)
    assert len(title) > 3

def test_client_banner_new_case():
    banner = core.banner()
    assert "ZAP" in banner or "Proxy" in banner