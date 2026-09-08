import pytest

def example_entry():
    # This stub mimics the 'example_entry' C function.
    # In the real application, import or implement the real example logic.
    return 42

def test_example():
    # Basic entry, testing at least one path
    ret = example_entry()
    print(f"Example returned: {ret}")
    assert isinstance(ret, int)

# Extra 'test done' message is not needed in pytest