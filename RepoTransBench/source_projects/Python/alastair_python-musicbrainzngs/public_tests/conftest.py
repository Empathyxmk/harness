import sys
import os

# Ensure the musicbrainzngs package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure the test helpers (like _common.py) are importable from test/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../test")))