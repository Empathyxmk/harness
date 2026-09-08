import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.mark.skip("Django fields not tested in public variant.")
def test_skip_django_field_1():
    pass

@pytest.mark.skip("Django fields not tested in public variant.")
def test_skip_django_field_2():
    pass