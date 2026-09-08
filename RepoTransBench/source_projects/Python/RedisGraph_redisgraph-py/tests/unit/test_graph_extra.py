import pytest
from redisgraph import graph
from redisgraph.node import Node
from redisgraph.edge import Edge

class DummyConnection:
    def execute_command(self, *args, **kwargs):
        return "EXECUTED"

def setup_graph():
    g = graph.Graph("G", DummyConnection())
    return g

def test_graph_add_node():
    g = setup_graph()
    n = Node(label="Person", properties={"name": "Alice"})
    g.add_node(n)
    assert n in g.nodes

def test_graph_add_edge():
    g = setup_graph()
    n1 = Node(label="Person", properties={"name": "Alice"})
    n2 = Node(label="Person", properties={"name": "Bob"})
    g.add_node(n1)
    g.add_node(n2)
    e = Edge(n1, "knows", n2)
    g.add_edge(e)
    assert e in g.edges

def test_graph_commit():
    g = setup_graph()
    n1 = Node(label="Person", properties={"name": "Alice"})
    n2 = Node(label="Person", properties={"name": "Bob"})
    g.add_node(n1)
    g.add_node(n2)
    e = Edge(n1, "knows", n2)
    g.add_edge(e)
    assert g.commit() == "EXECUTED"

def test_graph_delete():
    g = setup_graph()
    assert g.delete() == "EXECUTED"

def test_graph_query():
    g = setup_graph()
    assert g.query("MATCH (n) RETURN n") == "EXECUTED"