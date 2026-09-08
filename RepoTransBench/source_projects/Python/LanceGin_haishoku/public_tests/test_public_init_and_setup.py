import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_init_module_exists():
    assert os.path.exists("haishoku/__init__.py")

def test_alg_module_exists():
    assert os.path.exists("haishoku/alg.py")