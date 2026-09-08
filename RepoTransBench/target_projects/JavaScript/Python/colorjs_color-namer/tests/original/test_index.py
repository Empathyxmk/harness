import pytest

try:
    import src.namer as namer
    import chroma
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
    import namer  # type: ignore
    import chroma  # type: ignore

def test_namer_is_function():
    assert callable(namer.namer), "namer must be a function"

def test_namer_returns_sorted_named_arrays_for_color():
    result = namer.namer('#000')
    assert isinstance(result, dict)
    assert len(result) > 0
    for list_ in result.values():
        assert isinstance(list_, list)
    basic_entry = result['basic'][0]
    assert 'name' in basic_entry
    assert 'hex' in basic_entry
    assert 'distance' in basic_entry

def test_namer_handles_non_hex_input():
    result = namer.namer('blue')
    assert isinstance(result, dict)
    assert len(result) > 0

def test_namer_handles_pick_option():
    result = namer.namer('#000', pick=['pantone', 'basic'])
    keys = set(result.keys())
    assert 'pantone' in keys
    assert 'basic' in keys

def test_namer_handles_omit_option():
    result = namer.namer('#000', omit=['html'])
    assert 'html' not in result
    assert 'basic' in result

def test_namer_pick_precedence_over_omit():
    result = namer.namer('#000', pick=['html', 'pantone'], omit=['pantone'])
    assert set(result.keys()) == {'html'}

def test_namer_caches_results():
    options = {'pick': ['basic']}
    first = namer.namer('#000', **options)
    second = namer.namer('#000', **options)
    assert first == second

def test_namer_distance_deltae():
    result = namer.namer('#000', distance='deltaE')
    assert result is not None
    assert isinstance(result['basic'], list)
    assert 'distance' in result['basic'][0]

def test_namer_exports_chroma():
    chroma_func = getattr(namer, 'chroma', None)
    assert chroma_func is not None
    assert callable(chroma_func)
    assert chroma_func('red').hex() == '#ff0000'

def test_namer_exports_lists():
    lists = getattr(namer, 'lists', None)
    assert lists is not None
    assert 'ntc' in lists
    assert isinstance(lists['ntc'], list)

def test_namer_throws_on_unrecognized_color():
    with pytest.raises(Exception):
        namer.namer('notacolor')

def test_namer_accepts_chroma_object():
    color = chroma.Color('red')
    try:
        namer.namer(color)
    except Exception as e:
        pytest.fail(f"namer should not throw when given chroma object: {e}")