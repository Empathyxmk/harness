import sys
import os

# Ensure the project root is on sys.path, so 'import jd4' works in public tests.
PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "jd4", "__init__.py")))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)