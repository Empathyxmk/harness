import pytest
from gvanim.animation import Step, Animation, ParseException

def test_step_copy_and_repr_public():
    step1 = Step()
    step1.V.add(10)
    step1.E.add((10, 20))
    step1.lV[10] = "X"
    step1.lE[(10, 20)] = "EdgeAB"
    step2 = Step(step1)
    assert step2.V == step1.V
    assert step2.E == step1.E
    assert step2.lV == step1.lV
    assert step2.lE == step1.lE
    r = repr(step2)
    assert 'V' in r and 'E' in r

def test_node_format_basic_public():
    s = Step()
    s.V.add(5)
    s.lV[5] = "B"
    s.hV[5] = 'red'
    res = s.node_format(5)
    assert "label=" in res and "color=red" in res

def test_node_format_hidden_public():
    s = Step()
    res = s.node_format(123)
    assert "style=invis" in res

def test_edge_format_all_public():
    s = Step()
    e = (7, 8)
    s.E.add(e)
    s.lE[e] = "labelZ"
    s.hE[e] = "orange"
    res = s.edge_format(e)
    assert "label=" in res and "color=orange" in res

def test_edge_format_hidden_public():
    s = Step()
    res = s.edge_format((17, 28))
    assert "style=invis" in res

def test_animation_action_methods_public(monkeypatch):
    anim = Animation()
    # test all action appending with different numbers
    anim.next_step()
    anim.add_node(101)
    anim.highlight_node(201, color="purple")
    anim.label_node(201, "Z")
    anim.unlabel_node(201)
    anim.remove_node(201)
    anim.add_edge(101, 301)
    anim.highlight_edge(101, 301, color="pink")
    anim.label_edge(101, 301, "F")
    anim.unlabel_edge(101, 301)
    anim.remove_edge(101, 301)
    # No assertion needed, just check for exceptions

def test_animation_parse_good_public():
    anim = Animation()
    anim.parse([
        'an 17',
        'ae 17 18',
        'ln 17 labelB',
        'le 17 18 labelF',
        'hn 17',
        'he 17 18',
        'ns',
        'un 17',
        'ue 17 18',
        'rn 17',
        're 17 18'
    ])
    # no exception

def test_animation_parse_bad_public(monkeypatch):
    anim = Animation()
    with pytest.raises(ParseException):
        anim.parse(['badcmd 77'])

def test_animation_parse_bad_format_public(monkeypatch):
    anim = Animation()
    # insufficient args
    with pytest.raises(ParseException):
        anim.parse(['ae'])
    # invalid int conversion
    with pytest.raises(ParseException):
        anim.parse(['an invalidnum'])