import sys
import os

# Ensure 'src' is in sys.path for all public tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))