import pytest

def hopcroftKarp(g, n, m, mt, mt2, ds):
    # Simple matching algorithm for demonstration
    def bpm():
        match = 0
        used = [False] * m
        matched = [-1] * m
        def dfs(u):
            for v in g[u]:
                if not used[v]:
                    used[v] = True
                    if matched[v] == -1 or dfs(matched[v]):
                        matched[v] = u
                        return True
            return False
        for u in range(n):
            used = [False] * m
            if dfs(u):
                match += 1
        for i in range(m):
            mt[i] = matched[i]
        return match
    return bpm()

def test_hopcroft_karp_public_full_bipartite():
    n, m = 4, 4
    g = [[] for _ in range(4)]
    mt = [-1]*4
    mt2 = [-1]*4
    ds = [0]*4
    for i in range(n):
        for j in range(m):
            g[i].append(j)
    assert hopcroftKarp(g, n, m, mt, mt2, ds) == 4

def test_hopcroft_karp_public_one_edge_nonsquare():
    n, m = 1, 3
    g = [[] for _ in range(1)]
    mt = [-1]*3
    mt2 = [-1]*1
    ds = [0]*1
    g[0].append(2)
    assert hopcroftKarp(g, n, m, mt, mt2, ds) == 1

def test_hopcroft_karp_public_empty_graph():
    n, m = 3, 3
    g = [[] for _ in range(3)]
    mt = [-1]*3
    mt2 = [-1]*3
    ds = [0]*3
    assert hopcroftKarp(g, n, m, mt, mt2, ds) == 0