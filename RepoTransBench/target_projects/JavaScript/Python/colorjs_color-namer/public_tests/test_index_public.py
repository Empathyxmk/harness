import pytest

try:
    import src.namer as namer
    import chroma
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
    import namer  # type: ignore
    import chroma  # type: ignore

def test_namer_is_function_public():
    assert callable(namer.namer), "namer must be a function"

def test_namer_returns_sorted_named_arrays_for_color_public():
    result = namer.namer('#FFF')
    assert isinstance(result, dict)
    assert len(result) > 0
    for list_ in result.values():
        assert isinstance(list_, list)
    basic_entry = result['basic'][0]
    assert 'name' in basic_entry
    assert 'hex' in basic_entry
    assert 'distance' in basic_entry

def test_namer_handles_non_hex_input_public():
    result = namer.namer('green')
    assert isinstance(result, dict)
    assert len(result) > 0

def test_namer_handles_pick_option_public():
    result = namer.namer('#FFF', pick=['x11', 'html'])
    keys = set(result.keys())
    assert 'x11' in keys
    assert 'html' in keys

def test_namer_handles_omit_option_public():
    result = namer.namer('#FFF', omit=['x11'])
    assert 'x11' not in result
    assert 'basic' in result

def test_namer_pick_precedence_over_omit_public():
    result = namer.namer('#FFF', pick=['roygbiv', 'ntc'], omit=['ntc'])
    assert set(result.keys()) == {'roygbiv'}

def test_namer_caches_results_public():
    options = {'pick': ['html']}
    first = namer.namer('#FFF', **options)
    second = namer.namer('#FFF', **options)
    assert first == second

def test_namer_distance_deltae_public():
    result = namer.namer('#FFF', distance='deltaE')
    assert result is not None
    assert isinstance(result['basic'], list)
    assert 'distance' in result['basic'][0]

def test_namer_exports_chroma_public():
    chroma_func = getattr(namer, 'chroma', None)
    assert chroma_func is not None
    assert callable(chroma_func)
    assert chroma_func('blue').hex() == '#0000ff'

def test_namer_exports_lists_public():
    lists = getattr(namer, 'lists', None)
    assert lists is not None
    assert 'x11' in lists
    assert isinstance(lists['x11'], list)

def test_namer_throws_on_unrecognized_color_public():
    with pytest.raises(Exception):
        namer.namer('blorple')

def test_namer_accepts_chroma_object_public():
    color = chroma.Color(h=240, s=1, l=0.5)
    try:
        namer.namer(color)
    except Exception as e:
        pytest.fail(f"namer should not throw when given chroma object: {e}")