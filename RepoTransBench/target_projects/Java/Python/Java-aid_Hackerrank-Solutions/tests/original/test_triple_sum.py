import io
import sys
import pytest

# Implementation for testability - minimal to run the test logic
def remove_duplicates(arr):
    return sorted(set(arr))

def get_valid_index(arr, val):
    # Returns the last index i such that arr[i] <= val, or -1 if no such index
    left, right = 0, len(arr) - 1
    res = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] <= val:
            res = mid
            left = mid + 1
        else:
            right = mid - 1
    return res

def triplets(a, b, c):
    # Hackerrank version wants to count (p, q, r) with p in a, q in b, r in c and p <= q and r <= q
    # Remove duplicates and sort
    a, b, c = remove_duplicates(a), sorted(set(b)), remove_duplicates(c)
    count = 0
    ia, ic = 0, 0
    a_sorted = sorted(a)
    c_sorted = sorted(c)
    for q in b:
        while ia < len(a_sorted) and a_sorted[ia] <= q:
            ia += 1
        while ic < len(c_sorted) and c_sorted[ic] <= q:
            ic += 1
        count += ia * ic
    return count

def triple_sum_main(stdin=None, stdout=None):
    '''
    Accepts an input stream and output stream (for testability)
    '''
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout
    def input():
        return stdin.readline()
    lens = input().split()
    if len(lens) < 3 or not all(s.strip().isdigit() for s in lens):
        print(0, file=stdout)
        return
    lena, lenb, lenc = map(int, lens)
    a = list(map(int, input().split())) if lena > 0 else []
    b = list(map(int, input().split())) if lenb > 0 else []
    c = list(map(int, input().split())) if lenc > 0 else []
    res = triplets(a, b, c)
    print(res, file=stdout)

class TestTripleSum:
    def test_typical_case(self):
        a = [1, 3, 5]
        b = [2, 3]
        c = [1, 2, 3]
        expected = 8
        assert triplets(a, b, c) == expected

    def test_duplicate_values(self):
        a = [1, 3, 5, 3]
        b = [2, 3, 3]
        c = [1, 2, 3, 1]
        expected = 8
        assert triplets(a, b, c) == expected

    def test_all_zeros(self):
        a = [0, 0, 0]
        b = [0, 0]
        c = [0, 0]
        expected = 1
        assert triplets(a, b, c) == expected

    def test_empty_arrays(self):
        a = []
        b = []
        c = []
        expected = 0
        assert triplets(a, b, c) == expected

    def test_remove_duplicates(self):
        arr = [1, 1, 2, 2, 3, 3, 3]
        res = remove_duplicates(arr)
        assert len(res) == 3
        assert all(x in [1, 2, 3] for x in res)

    def test_get_valid_index(self):
        arr = [1, 2, 3, 4, 5]
        assert get_valid_index(arr, 3) == 2
        assert get_valid_index(arr, 6) == 4
        assert get_valid_index(arr, 0) == -1
        assert get_valid_index([2], 2) == 0

    def test_main_example_input(self):
        input_str = "3 2 3\n1 3 5\n2 3\n1 2 3\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        triple_sum_main(stdin=stdin, stdout=stdout)
        output = stdout.getvalue().strip()
        assert "8" in output

    def test_main_with_empty_arrays(self):
        input_str = "0 0 0\n\n\n\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        triple_sum_main(stdin=stdin, stdout=stdout)
        output = stdout.getvalue().strip()
        assert "0" in output