import io
import sys
import pytest

def climbing_leaderboard(ranked, player):
    # Remove duplicate scores, keep descending order (like leaderboard)
    ranked = sorted(set(ranked), reverse=True)
    result = []
    n = len(ranked)
    idx = n-1
    for score in player:
        while idx >= 0 and score >= ranked[idx]:
            idx -= 1
        result.append(idx+2)
    return result

def binary_search(arr, val):
    # Decreasing sorted array, returns index where arr[index] <= val < arr[index-1] (leftmost)
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left+right)//2
        if arr[mid] == val:
            return mid
        elif arr[mid] > val:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def climbing_the_leaderboard_main(stdin=None, stdout=None):
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout
    def input():
        return stdin.readline()
    n = int(input())
    ranked = list(map(int, input().split()))
    m = int(input())
    player = list(map(int, input().split()))
    result = climbing_leaderboard(ranked, player)
    for val in result:
        print(val, file=stdout)

class TestClimbingTheLeaderboard:
    def test_typical_case(self):
        scores = [100,100,50,40,40,20,10]
        alice = [5,25,50,120]
        expected = [6,4,2,1]
        assert climbing_leaderboard(scores, alice) == expected

    def test_all_scores_same(self):
        scores = [100,100,100]
        alice = [50,100,101]
        expected = [2,1,1]
        assert climbing_leaderboard(scores, alice) == expected

    def test_alice_all_lower(self):
        scores = [60,30,10]
        alice = [5,3]
        expected = [4,4]
        assert climbing_leaderboard(scores, alice) == expected

    def test_alice_all_higher(self):
        scores = [40,20,10]
        alice = [50]
        expected = [1]
        assert climbing_leaderboard(scores, alice) == expected

    def test_single_element_scores(self):
        scores = [100]
        alice = [100,101,99]
        expected = [1,1,2]
        assert climbing_leaderboard(scores, alice) == expected

    def test_binary_search(self):
        a = [100,90,80,70,70,60]
        assert binary_search(a, 70) == 3
        assert binary_search(a, 85) == -1
        assert binary_search(a, 95) == -1
        assert binary_search(a, 50) == -1

    def test_main_typical_case(self):
        input_str = "7\n100 100 50 40 40 20 10\n4\n5 25 50 120\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        climbing_the_leaderboard_main(stdin=stdin, stdout=stdout)
        outstr = stdout.getvalue()
        assert "1" in outstr and "6" in outstr