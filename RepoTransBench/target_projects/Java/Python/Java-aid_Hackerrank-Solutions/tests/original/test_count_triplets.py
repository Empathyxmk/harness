import io
import sys
import pytest
from collections import defaultdict

# Direct implementation for testability
def count_triplets(arr, r):
    '''
    Given an array, counts the number of triplets (i, j, k) with i<j<k such that arr[j]=arr[i]*r, arr[k]=arr[j]*r
    '''
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

def count_triplets_private(arr, r):
    return count_triplets(arr, r)

def count_triplets_main(stdin=None, stdout=None):
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout
    def input():
        return stdin.readline()
    first_line = input()
    if first_line.strip() == '':
        print(0, file=stdout)
        return
    parts = first_line.strip().split()
    if len(parts) < 2:
        print(0, file=stdout)
        return
    n, r = map(int, parts)
    arr_line = input().strip()
    if n == 0 or arr_line == '':
        arr = []
    else:
        arr = list(map(int, arr_line.split()))
    res = count_triplets(arr, r)
    print(res, file=stdout)

class TestCountTriplets:
    def invoke(self, arr, r):
        return count_triplets_private(arr, r)

    def test_typical_case(self):
        arr = [1,2,2,4]
        r = 2
        expected = 2
        assert self.invoke(arr, r) == expected

    def test_all_ones_r1(self):
        arr = [1,1,1,1]
        r = 1
        assert self.invoke(arr, r) == 4

    def test_no_triplets(self):
        arr = [1,2,4,8]
        r = 3
        assert self.invoke(arr, r) == 0

    def test_single_element(self):
        arr = [7]
        r = 2
        assert self.invoke(arr, r) == 0

    def test_empty_list(self):
        arr = []
        assert self.invoke(arr, 2) == 0

    def test_main_typical_case(self):
        input_str = "4 2\n1 2 2 4\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        count_triplets_main(stdin=stdin, stdout=stdout)
        output = stdout.getvalue().strip()
        assert output.endswith("2")

    def test_main_empty(self):
        input_str = "0 2\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        count_triplets_main(stdin=stdin, stdout=stdout)
        output = output = stdout.getvalue().replace("\n", "").strip()
        assert output.endswith("0")