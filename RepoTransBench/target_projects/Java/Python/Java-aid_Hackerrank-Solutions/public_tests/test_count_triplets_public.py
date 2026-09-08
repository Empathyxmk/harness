from collections import defaultdict

def count_triplets(arr, r):
    v2 = defaultdict(int)
    v3 = defaultdict(int)
    count = 0
    for k in arr:
        if k in v3:
            count += v3[k]
        if k in v2:
            v3[k*r] += v2[k]
        v2[k*r] += 1
    return count

def test_case_ratio2():
    arr = [2, 4, 8, 16, 32, 4, 8]
    r = 2
    assert count_triplets(arr, r) == 6

def test_case_ratio3():
    arr = [9, 27, 81, 243, 3, 9, 27]
    r = 3
    assert count_triplets(arr, r) == 6

def test_case_no_triplets():
    arr = [1, 2, 5, 7]
    r = 3
    assert count_triplets(arr, r) == 0