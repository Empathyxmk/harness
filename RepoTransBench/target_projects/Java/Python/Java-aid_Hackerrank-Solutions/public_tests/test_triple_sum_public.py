def triplets(a, b, c):
    a, b, c = sorted(set(a)), sorted(set(b)), sorted(set(c))
    ai = ci = 0
    total = 0
    for val in b:
        while ai < len(a) and a[ai] <= val:
            ai += 1
        while ci < len(c) and c[ci] <= val:
            ci += 1
        total += ai * ci
    return total

def test_public_input1():
    a = [2, 3, 4, 4, 7]
    b = [1, 2, 5, 5]
    c = [3, 3, 5, 8]
    # The expected value was 5 in the Java public test
    assert triplets(a, b, c) == 5

def test_public_input2():
    a = [3, 4, 7, 7, 10]
    b = [1, 3, 5, 7, 9]
    c = [2, 3, 6, 9]
    assert triplets(a, b, c) == 9