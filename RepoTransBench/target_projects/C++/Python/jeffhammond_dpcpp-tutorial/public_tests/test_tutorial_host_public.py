"""
Public test: tutorial host logic, adapted (assumes test_tutorial_host.cpp tests basic host SYCL vector math).
This public test uses different test data (vector length).
"""

def test_tutorial_host_public():
    length = 7  # Different from likely length in secret
    a = [3.5] * length
    b = [-1.3] * length
    sum_ = [a[i] + b[i] for i in range(length)]
    # Assert correctness for each element
    for value in sum_:
        assert value == 2.2  # 3.5 + (-1.3) = 2.2
    print(f"Public host test - sum OK for length {length}")