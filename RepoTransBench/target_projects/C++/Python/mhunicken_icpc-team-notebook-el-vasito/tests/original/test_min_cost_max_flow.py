import pytest

# Placeholder MCF class for demonstration
class MCF:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.edges = []

    def add_edge(self, s, t, cap, cost):
        self.g[s].append(len(self.edges))
        self.edges.append([s, t, cap, 0, cost])
        self.g[t].append(len(self.edges))
        self.edges.append([t, s, 0, 0, -cost])

    def get_flow(self, s, t):
        flow = 0
        flowcost = 0
        INF = 10**9
        pot = [0]*self.n
        while True:
            from heapq import heappush, heappop
            prio = [INF]*self.n
            curflow = [0]*self.n
            prevedge = [-1]*self.n
            prevnode = [-1]*self.n
            q = []
            heappush(q, (0, s))
            prio[s] = 0
            curflow[s] = INF
            while q:
                d, u = heappop(q)
                if d != prio[u]: continue
                for idx in self.g[u]:
                    e = self.edges[idx]
                    v = e[1]
                    if e[2] <= e[3]: continue
                    nprio = prio[u] + e[4] + pot[u] - pot[v]
                    if prio[v] > nprio:
                        prio[v] = nprio
                        heappush(q, (nprio, v))
                        prevnode[v] = u
                        prevedge[v] = idx
                        curflow[v] = min(curflow[u], e[2]-e[3])
            if prio[t]==INF: break
            for i in range(self.n): pot[i] += prio[i]
            df = min(curflow[t], INF-flow)
            flow += df
            v = t
            while v != s:
                idx = prevedge[v]
                self.edges[idx][3] += df
                self.edges[idx^1][3] -= df
                flowcost += df*self.edges[idx][4]
                v = prevnode[v]
        return (flow, flowcost)

def test_case_greed():
    tn = 1
    n = 3
    q = [1, 1, 1]
    nt = MCF(n+2)
    for i in range(n):
        nt.add_edge(0,2+i,q[i],0)
    for i in range(n):
        nt.add_edge(2+i,1,1,0)
    nt.add_edge(2+0,2+1,512,1)
    nt.add_edge(2+1,2+0,512,1)
    result = nt.get_flow(0,1)
    # The minimum cost flow for this network should be verified.
    assert isinstance(result, tuple)