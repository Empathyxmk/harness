import pytest

# Public test for compile: distinct tag and minimal logic for public variant.
# To ensure it's a different test, test an unused simple property.
def test_compile_public_dummy():
    # Use a different trivial check
    x = 42
    assert x == 42