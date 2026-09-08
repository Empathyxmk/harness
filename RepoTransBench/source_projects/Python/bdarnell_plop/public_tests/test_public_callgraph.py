import unittest
from plop.callgraph import CallGraph, Node

class PublicSimpleCallgraphTest(unittest.TestCase):
    def setUp(self):
        graph = CallGraph()
        # Different node IDs/structure from original test
        graph.add_stack([Node(10), Node(20)], dict(weight=2))
        graph.add_stack([Node(10), Node(30)], dict(weight=8))
        graph.add_stack([Node(10), Node(20), Node(30)], dict(weight=4))
        graph.add_stack([Node(18), Node(10), Node(40)], dict(weight=6))
        self.graph = graph

    def test_basic_attrs(self):
        self.assertEqual(len(self.graph.nodes), 4)
        self.assertEqual(len(self.graph.edges), 5)

    def test_top_edges(self):
        top_edges = self.graph.get_top_edges('weight', 2)
        summary = [(e.parent.id, e.child.id, e.weights['weight']) for e in top_edges]
        # Different edge weights and ids from main test
        self.assertEqual(summary, [
            (10, 30, 12),
            (10, 20, 6),
        ])

    def test_top_nodes(self):
        top_nodes = self.graph.get_top_nodes('weight', 3)
        summary = [(n.id, n.weights['weight']) for n in top_nodes]
        self.assertEqual(summary, [
            (30, 12),
            (10, 0),
            (20, 2),
        ])