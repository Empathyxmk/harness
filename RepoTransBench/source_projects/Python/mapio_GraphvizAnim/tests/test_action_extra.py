import gvanim.action as ga
from gvanim.animation import Step

def test_add_node_action():
    s = [Step()]
    ga.AddNode(42)(s)
    assert 42 in s[-1].V

def test_highlight_node_and_label_node():
    s = [Step()]
    ga.HighlightNode(2, color='blue')(s)
    ga.LabelNode(2, "lbl")(s)
    assert 2 in s[-1].hV and 2 in s[-1].lV

def test_unlabel_and_remove_node():
    s = [Step()]
    ga.AddNode(1)(s)
    ga.LabelNode(1, "tok")(s)
    ga.UnlabelNode(1)(s)
    assert 1 not in s[-1].lV
    ga.RemoveNode(1)(s)
    assert 1 not in s[-1].V

def test_add_edge_and_highlight_label_unlabel_remove():
    s = [Step()]
    ga.AddNode(3)(s)
    ga.AddNode(4)(s)
    ga.AddEdge(3, 4)(s)
    ga.HighlightEdge(3, 4, color='green')(s)
    ga.LabelEdge(3, 4, "X")(s)
    assert (3, 4) in s[-1].E and (3, 4) in s[-1].hE and (3, 4) in s[-1].lE
    ga.UnlabelEdge(3, 4)(s)
    ga.RemoveEdge(3, 4)(s)
    assert (3, 4) not in s[-1].E