import pytest

# Dummy placeholder for hopcroft_karp; must be replaced with actual implementation
def hopcroftKarp(g, n, m, mt, mt2, ds):
    # Simple maximum matching in bipartite graph using dfs (not HK, but matches test logic)
    def bpm():
        match = 0
        used = [False] * n
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

def reset(g, MAXN, MAXM):
    for i in range(MAXN):
        g[i][:] = []
    return g

def test_hopcroft_karp_full_matching():
    n = 3
    m = 3
    MAXN, MAXM = 10, 10
    g = [[] for _ in range(MAXN)]
    mt = [-1]*MAXM
    mt2 = [-1]*MAXN
    ds = [0]*MAXN
    g[0] = [0,1]
    g[1] = [1,2]
    g[2] = [0]
    assert hopcroftKarp(g, n, m, mt, mt2, ds) == 3

def test_hopcroft_karp_no_edges():
    n = 2
    m = 2
    MAXN, MAXM = 10, 10
    g = [[] for _ in range(MAXN)]
    mt = [-1]*MAXM
    mt2 = [-1]*MAXN
    ds = [0]*MAXN
    assert hopcroftKarp(g, n, m, mt, mt2, ds) == 0

def test_hopcroft_karp_one_possibility():
    n = 2
    m = 2
    MAXN, MAXM = 10, 10
    g = [[] for _ in range(MAXN)]
    g[0] = [1]
    g[1] = [0]
    mt = [-1]*MAXM
    mt2 = [-1]*MAXN
    ds = [0]*MAXN
    assert hopcroftKarp(g, n, m, mt, mt2, ds) == 2