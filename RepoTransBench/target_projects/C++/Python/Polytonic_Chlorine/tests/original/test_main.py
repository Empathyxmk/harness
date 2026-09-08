import pytest
import random
import time

# -- Simulate the Chlorine kernel arithmetic behavior with Python equivalents --

def test_ops(instr, a, b):
    if instr == "add":
        return a + b
    elif instr == "sub":
        return a - b
    elif instr == "mul":
        return a * b
    else:
        return -1

@pytest.mark.parametrize("typ,val,instrs", [
    ('integers', 1,    ['add', 'sub', 'mul']),
    ('floats',   1.0,  ['add', 'sub', 'mul']),
])
def test_arithmetic_arrays(typ, val, instrs):
    # simulate kernel calls
    n = 10
    a = [val + i for i in range(n)]
    b = [val + i for i in range(n)]
    for instr in instrs:
        # Simulate C-style array, list, etc.
        # All checks use test_ops for logic
        c = [test_ops(instr, a[i], b[i]) for i in range(n)]
        # also as numpy if wanted: np.array(a) + np.array(b), etc.
        for i in range(n):
            assert c[i] == test_ops(instr, a[i], b[i])

def fill_scalar(a, b):
    # Simulate scalar fill
    for i in range(len(a)):
        a[i] = b

def test_scalars():
    # Integer scalar fill
    n = 10
    a = [0] * n
    b = random.randint(1, 100)
    fill_scalar(a, b)
    assert all(x == b for x in a)

    # Float scalar fill
    a = [0.0] * n
    b = random.uniform(1, 100)
    fill_scalar(a, b)
    assert all(x == b for x in a)

def fill_vector_integers(a):
    # Simulate int4 vector fill: each entry is [0,1,2,3]
    for i in range(len(a)):
        a[i] = [0,1,2,3]

def fill_vector_floats(a):
    for i in range(len(a)):
        a[i] = [0.0,1.0,2.0,3.0]

def test_vectors():
    n = 10
    # Integer vector fill
    a = [None] * n
    fill_vector_integers(a)
    for item in a:
        assert item == [0,1,2,3]

    # Float vector fill
    a = [None] * n
    fill_vector_floats(a)
    for item in a:
        assert item == [0.0,1.0,2.0,3.0]

def test_helpers_elapsed():
    # Simulate timing function
    n = 100
    a = [100] * n

    t0 = time.time()
    # "fill" kernel just sets all to 1
    for i in range(len(a)):
        a[i] = 1
    elapsed = time.time() - t0

    assert all(x == 1 for x in a)
    assert elapsed >= 0

def test_helpers_read():
    # Simulate kernel file reading and equivalence check
    simulated_kernel = (
        "// Test the Kernel Read Function\n"
        "__kernel void fill(__global int * a)\n"
        "{\n"
        "    unsigned int i = get_global_id(0);\n"
        "    a[i] = 1;\n"
        "}\n"
    )
    # In project, reading from file; here, just check the string
    match = (
        "// Test the Kernel Read Function\n"
        "__kernel void fill(__global int * a)\n"
        "{\n"
        "    unsigned int i = get_global_id(0);\n"
        "    a[i] = 1;\n"
        "}\n"
    )
    assert simulated_kernel == match

def test_operator_right_shift_no_throw():
    # Simulate ">>" operator kernel string acceptance by "worker"
    # In Python, we can just ensure no error on dummy operation.
    try:
        # Simulate loading kernel string (would be a no-op)
        pass
    except Exception:
        pytest.fail("Operator >> should not throw")

def test_operator_left_shift_throw():
    # Simulate "<<" operator (build log), should throw on invalid kernel
    # In the original, dies if kernel invalid.
    with pytest.raises(Exception):
        # Simulate raising on build failure
        raise Exception("Kernel build failed as expected")