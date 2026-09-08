import pytest
from gvanim.animation import Step, Animation, ParseException

def test_step_copy_and_repr():
    step1 = Step()
    step1.V.add(1)
    step1.E.add((1, 2))
    step1.lV[1] = "A"
    step1.lE[(1, 2)] = "EdgeLabel"
    step2 = Step(step1)
    assert step2.V == step1.V
    assert step2.E == step1.E
    assert step2.lV == step1.lV
    assert step2.lE == step1.lE
    r = repr(step2)
    assert 'V' in r and 'E' in r

def test_node_format_basic():
    s = Step()
    s.V.add(1)
    s.lV[1] = "A"
    s.hV[1] = 'blue'
    res = s.node_format(1)
    assert "label=" in res and "color=blue" in res

def test_node_format_hidden():
    s = Step()
    res = s.node_format(99)
    assert "style=invis" in res

def test_edge_format_all():
    s = Step()
    e = (1, 2)
    s.E.add(e)
    s.lE[e] = "lbl"
    s.hE[e] = "green"
    res = s.edge_format(e)
    assert "label=" in res and "color=green" in res

def test_edge_format_hidden():
    s = Step()
    res = s.edge_format((3, 4))
    assert "style=invis" in res

def test_animation_action_methods(monkeypatch):
    anim = Animation()
    # test all action appending
    anim.next_step()
    anim.add_node(1)
    anim.highlight_node(2, color="yellow")
    anim.label_node(2, "Y")
    anim.unlabel_node(2)
    anim.remove_node(2)
    anim.add_edge(1, 3)
    anim.highlight_edge(1, 3, color="green")
    anim.label_edge(1, 3, "E")
    anim.unlabel_edge(1, 3)
    anim.remove_edge(1, 3)
    # there is no assertion, just check for exceptions

def test_animation_parse_good():
    anim = Animation()
    anim.parse([
        'an 7',
        'ae 7 8',
        'ln 7 labelA',
        'le 7 8 labelE',
        'hn 7',
        'he 7 8',
        'ns',
        'un 7',
        'ue 7 8',
        'rn 7',
        're 7 8'
    ])
    # no exception

def test_animation_parse_bad(monkeypatch):
    anim = Animation()
    with pytest.raises(ParseException):
        anim.parse(['foobar 1'])

def test_animation_parse_bad_format(monkeypatch):
    anim = Animation()
    # insufficient args
    with pytest.raises(ParseException):
        anim.parse(['ae 2'])
    # invalid int conversion
    with pytest.raises(ParseException):
        anim.parse(['an notanint'])