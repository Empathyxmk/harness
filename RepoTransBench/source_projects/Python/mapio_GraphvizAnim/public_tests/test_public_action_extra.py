import gvanim.action as ga
from gvanim.animation import Step

def test_add_node_action_public():
    s = [Step()]
    ga.AddNode(12)(s)
    assert 12 in s[-1].V

def test_highlight_node_and_label_node_public():
    s = [Step()]
    ga.HighlightNode(20, color='red')(s)
    ga.LabelNode(20, "lbl2")(s)
    assert 20 in s[-1].hV and 20 in s[-1].lV

def test_unlabel_and_remove_node_public():
    s = [Step()]
    ga.AddNode(9)(s)
    ga.LabelNode(9, "zzz")(s)
    ga.UnlabelNode(9)(s)
    assert 9 not in s[-1].lV
    ga.RemoveNode(9)(s)
    assert 9 not in s[-1].V

def test_add_edge_and_highlight_label_unlabel_remove_public():
    s = [Step()]
    ga.AddNode(6)(s)
    ga.AddNode(13)(s)
    ga.AddEdge(6, 13)(s)
    ga.HighlightEdge(6, 13, color='purple')(s)
    ga.LabelEdge(6, 13, "Y")(s)
    assert (6, 13) in s[-1].E and (6, 13) in s[-1].hE and (6, 13) in s[-1].lE
    ga.UnlabelEdge(6, 13)(s)
    ga.RemoveEdge(6, 13)(s)
    assert (6, 13) not in s[-1].E