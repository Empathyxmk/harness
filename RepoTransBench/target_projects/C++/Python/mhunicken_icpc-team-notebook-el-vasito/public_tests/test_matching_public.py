import pytest

def max_matching(n, m, g):
    # Simple greedy matching with DFS augmenting
    result = []
    mat = [-1]*m
    vis = [0]*n
    was = 1
    used = [False]*m
    for i in range(n):
        for j in g[i]:
            if mat[j] == -1 and not used[j]:
                mat[j] = i
                used[j] = True
                break
    def dfs(x):
        for y in g[x]:
            if mat[y] == -1 or dfs(mat[y]):
                mat[y] = x
                return True
        return False
    for z in range(n):
        found = False
        for i in range(n):
            if all(p[0] != i for p in result) and dfs(i):
                found = True
        if not found:
            break
    for j in range(m):
        if mat[j] != -1:
            result.append((mat[j], j))
    return result

def test_public_matching_1():
    n, m = 3, 3
    g = [[0,1,2],[0,1,2],[0,1,2]]
    r = max_matching(n, m, g)
    assert len(r) == 3

def test_public_matching_2():
    n, m = 2, 3
    g = [[0],[]]
    r = max_matching(n, m, g)
    assert len(r) == 1

def test_public_matching_3():
    n, m = 4, 4
    g = []
    for i in range(4):
        g.append([i, (i+1)%4])
    r = max_matching(n, m, g)
    assert len(r) == 4

def test_public_matching_4():
    n, m = 2, 5
    g = [[],[2]]
    r = max_matching(n, m, g)
    assert len(r) == 1