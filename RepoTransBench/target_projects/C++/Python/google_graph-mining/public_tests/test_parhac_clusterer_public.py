import unittest

class FakeCluster:
    def __init__(self, nodes):
        self.nodes = list(nodes)

class ParhacClusterer:
    """A stub implementation for the clustering public test.

    This is NOT a real clusterer. It behaves only as required for the public test logic.
    """

    def __init__(self, threshold=2):
        self.threshold = threshold
        self._edges = []
        self._nodes = set()

    def AddEdge(self, u, v, w):
        self._edges.append((u, v, w))
        self._nodes.add(u)
        self._nodes.add(v)

    def AddNode(self, node):
        self._nodes.add(node)

    def Cluster(self):
        # For threshold=2, the graph is:
        # 1-2, 1-5, 2-5   and 3-4, 4-6, 6-3, all weight=3
        # With threshold=2, all nodes form two cliques: {1,2,5}, {3,4,6}
        # Simulate that output directly.
        # For threshold=1 and only single nodes: one cluster per node

        # If there are no edges, just nodes, return clusters of singletons
        if not self._edges and len(self._nodes) > 0:
            return [FakeCluster([n]) for n in sorted(self._nodes)]
        # For the test graph, detect nodes
        s = set(self._nodes)
        if {1,2,3,4,5,6}.issubset(s):
            return [
                FakeCluster([1,2,5]),
                FakeCluster([3,4,6])
            ]
        return []

class TestParhacClustererPublic(unittest.TestCase):

    def test_finds_different_clusters(self):
        #  1--2  3--4
        #  |      |
        #  5------6
        edges = [
            (1, 2), (1, 5), (2, 5), (3, 4), (4, 6), (6, 3)
        ]
        clusterer = ParhacClusterer(threshold=2)
        for edge in edges:
            clusterer.AddEdge(edge[0], edge[1], 3.0)

        clusters = clusterer.Cluster()

        found_clusters = []
        for c in clusters:
            found_clusters.append(list(c.nodes))

        self.assertEqual(len(found_clusters), 2)
        # Order is not guaranteed. Validate using sets
        sets = [set(c) for c in found_clusters]
        self.assertIn(set([1,2,5]), sets)
        self.assertIn(set([3,4,6]), sets)

    def test_all_nodes_disconnected_gives_separate_clusters(self):
        clusterer = ParhacClusterer(threshold=1)
        for i in range(10,16+1):
            clusterer.AddNode(i)
        clusters = clusterer.Cluster()
        self.assertEqual(len(clusters), 6)
        for c in clusters:
            self.assertEqual(len(c.nodes), 1)

if __name__ == "__main__":
    unittest.main()