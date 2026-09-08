def climbing_leaderboard(ranked, player):
    ranked = sorted(set(ranked), reverse=True)
    result = []
    n = len(ranked)
    idx = n-1
    for score in player:
        while idx >= 0 and score >= ranked[idx]:
            idx -= 1
        result.append(idx+2)
    return result

def test_custom_case1():
    ranked = [120, 100, 100, 50, 40, 40, 20, 10]
    player = [5, 25, 45, 60, 105, 130]
    expected = [8, 6, 4, 4, 2, 1]
    assert climbing_leaderboard(ranked, player) == expected

def test_custom_case2():
    ranked = [200, 180, 180, 170, 160, 160, 150, 140]
    player = [130, 135, 150, 175, 190, 210]
    expected = [9, 9, 7, 4, 2, 1]
    assert climbing_leaderboard(ranked, player) == expected