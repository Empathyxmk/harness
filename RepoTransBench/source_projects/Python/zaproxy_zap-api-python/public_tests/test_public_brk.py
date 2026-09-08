import sys
import os
import pytest

# Ensure src directory is on PYTHONPATH for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from zapv2 import brk as brk_module

def test_brk_add_break_point_diff_data():
    # Add a different break rule than the existing test
    url = "http://public.example.com/login"
    method = "POST"
    response = brk_module.add_break_point(url, method)
    assert response["status"] == "OK"
    assert response["method"] == method
    assert response["url"].startswith("http://public.")

def test_brk_remove_break_point_diff_data():
    brk_id = "customBrk2"
    response = brk_module.remove_break_point(brk_id)
    assert response["status"] == "REMOVED"
    assert response["id"] == brk_id