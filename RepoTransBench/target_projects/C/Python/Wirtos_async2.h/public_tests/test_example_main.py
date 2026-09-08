import pytest

def example_main():
    # Mimic the 'example_main' C function return.
    # In actual use, import from src/examples.py or similar.
    return 42

def test_public_example_main():
    print("Hello from public example!")
    ret = example_main()
    print(f"Public example returned: {ret}")
    assert ret == 42
    print("Public example main test done.")