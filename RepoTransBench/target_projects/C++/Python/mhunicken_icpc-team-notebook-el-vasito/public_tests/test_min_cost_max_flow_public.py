import pytest
import heapq

class Edge:
    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.f = 0
        self.cost = cost

class MCF:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.pot = [0]*n

    def add_edge(self, s, t, cap, cost):
        self.g[s].append(Edge(t, len(self.g[t]), cap, cost))
        self.g[t].append(Edge(s, len(self.g[s])-1, 0, -cost))

    def mincostflow(self, s, t, maxf):
        prio = [0]*self.n
        curflow = [0]*self.n
        prevedge = [0]*self.n
        prevnode = [0]*self.n
        INF = 10**18
        flow = 0
        flow_cost = 0
        pot = [0]*self.n
        while flow < maxf:
            prio = [INF]*self.n
            curflow = [0]*self.n
            prevedge = [-1]*self.n
            prevnode = [-1]*self.n
            prio[s] = 0
            curflow[s] = INF
            q = [(0, s)]
            heapq.heapify(q)
            while q:
                d, u = heapq.heappop(q)
                if d != prio[u]:
                    continue
                for i,e in enumerate(self.g[u]):
                    v = e.to
                    if e.f >= e.cap:
                        continue
                    nprio = prio[u] + e.cost + pot[u] - pot[v]
                    if prio[v] > nprio:
                        prio[v] = nprio
                        heapq.heappush(q, (nprio, v))
                        prevnode[v] = u
                        prevedge[v] = i
                        curflow[v] = min(curflow[u], e.cap-e.f)
            if prio[t] == INF:
                break
            for i in range(self.n):
                pot[i] += prio[i]
            df = min(curflow[t], maxf-flow)
            flow += df
            cost = 0
            v = t
            while v != s:
                e = self.g[prevnode[v]][prevedge[v]]
                cost += e.cost * df
                e.f += df
                self.g[v][e.rev].f -= df
                v = prevnode[v]
            flow_cost += cost
        return (flow, flow_cost)

def test_mcf_public1():
    mcf = MCF(4)
    mcf.add_edge(0,1,2,1)
    mcf.add_edge(0,2,3,2)
    mcf.add_edge(1,3,2,2)
    mcf.add_edge(2,3,3,1)
    flow, cost = mcf.mincostflow(0,3,5)
    assert flow == 5 and cost == 15

def test_mcf_public2():
    mcf = MCF(3)
    mcf.add_edge(0,1,2,5)
    flow, cost = mcf.mincostflow(0,2,2)
    assert flow == 0 and cost == 0

def test_mcf_public3():
    mcf = MCF(4)
    mcf.add_edge(0,1,10,0)
    mcf.add_edge(1,2,5,0)
    mcf.add_edge(2,3,10,0)
    mcf.add_edge(1,3,1,0)
    flow, cost = mcf.mincostflow(0,3,10)
    assert flow == 6 and cost == 0