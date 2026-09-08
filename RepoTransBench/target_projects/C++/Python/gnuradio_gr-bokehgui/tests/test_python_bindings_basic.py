# For backward compatibility, directly import from original/ location to allow both:
# - python -m unittest discover -s tests
# - pytest tests/
from tests.original.test_python_bindings_basic import *