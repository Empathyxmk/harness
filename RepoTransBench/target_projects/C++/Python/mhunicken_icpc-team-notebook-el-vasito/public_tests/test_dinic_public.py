import pytest

# Dummy Dinic implementation for demonstration (replace for real code!)
class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.cap = {}

    def add_edge(self, u, v, c):
        self.g[u].append((v, c))
        self.cap[(u, v)] = self.cap.get((u, v), 0) + c
        self.g[v].append((u, 0))
        self.cap[(v, u)] = self.cap.get((v, u), 0)

    def max_flow(self, s, t):
        from collections import deque
        flow = 0
        INF = 1 << 60
        while True:
            level = [None] * self.n
            q = deque([s])
            level[s] = 0
            while q:
                u = q.popleft()
                for v, c in self.g[u]:
                    if level[v] is None and self.cap.get((u, v), 0) > 0:
                        level[v] = level[u] + 1
                        q.append(v)
            if level[t] is None:
                break
            ptr = [0] * self.n
            def dfs(u, pushed):
                if u == t or pushed == 0:
                    return pushed
                for i in range(ptr[u], len(self.g[u])):
                    v, _ = self.g[u][i]
                    if level.get(v, 0) == level[u]+1 and self.cap.get((u, v), 0) > 0:
                        tr = dfs(v, min(pushed, self.cap[(u, v)]))
                        if tr > 0:
                            self.cap[(u, v)] -= tr
                            self.cap[(v, u)] += tr
                            return tr
                    ptr[u] += 1
                return 0
            pushed = dfs(s, INF)
            while pushed:
                flow += pushed
                pushed = dfs(s, INF)
        return flow

def test_public_dinic_1():
    d = Dinic(4)
    d.add_edge(0,1,10)
    d.add_edge(0,2,5)
    d.add_edge(1,2,15)
    d.add_edge(1,3,10)
    d.add_edge(2,3,10)
    assert d.max_flow(0,3) == 15

def test_public_dinic_2():
    e = Dinic(3)
    e.add_edge(0,0,100)
    e.add_edge(1,2,11)
    assert e.max_flow(0,2) == 0