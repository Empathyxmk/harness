import pytest

# These functions are specific to the public test and should not interfere with original 'custom_math'
def custom_add_public(x, y):
    return x + y

def custom_multiply_public(x, y):
    return x * y

def test_custom_add_public_test():
    print("Running public test_custom_public.c ...")
    assert custom_add_public(10, 11) == 21, f"Expected 21, got {custom_add_public(10, 11)}"
    assert custom_add_public(-2, 5) == 3, f"Expected 3, got {custom_add_public(-2, 5)}"

def test_custom_multiply_public_test():
    assert custom_multiply_public(3, 6) == 18, f"Expected 18, got {custom_multiply_public(3, 6)}"
    assert custom_multiply_public(-3, 2) == -6, f"Expected -6, got {custom_multiply_public(-3, 2)}"
    print("test_custom_public passed!")