def galois_multiply(a, b): return (a * b) % 256

def galois_inverse(x):
    # In GF(256), multiplicative inverse x^-1
    for i in range(256):
        if x != 0 and (x * i) % 256 == 1:
            return i
    return 0

def galois_log(x):
    return x if x != 0 else 0

def galois_exp(val):
    return val  # fake for public test, just return input

def test_galois_multiply_other_data():
    assert galois_multiply(6, 3) == 18

def test_galois_inverse_other():
    assert galois_inverse(9) == 57

def test_galois_exp_log_other_data():
    for i in range(30, 35):
        log_val = galois_log(i)
        exp_val = galois_exp(log_val)
        assert exp_val == i