import pytest

try:
    from src.parser import parser
except ImportError:
    import sys
    parser = sys.modules.get('parser', None)

def test_parse_handle_tags_and_chars():
    events = []
    parser('<div class="a">hi<b>bye</b><!--comment--></div>', {
        'start': lambda tag, attrs, unary: events.append(['start', tag, attrs, unary]),
        'end': lambda tag: events.append(['end', tag]),
        'chars': lambda text: events.append(['chars', text]),
        'comment': lambda c: events.append(['comment', c])
    })
    assert events == [
        ['start', 'div', {'class': 'a'}, False],
        ['chars', 'hi'],
        ['start', 'b', {}, False],
        ['chars', 'bye'],
        ['end', 'b'],
        ['comment', 'comment'],
        ['end', 'div'],
    ]

def test_handle_unary_tags():
    events = []
    parser('<img src="x"/>', {
        'start': lambda tag, attrs, unary: events.append([tag, unary, attrs]),
        'end': lambda tag: events.append(['end', tag])
    })
    assert events[0][0] == 'img'
    assert events[0][1] is True
    assert events[0][2]['src'] == 'x'

def test_handle_tags_with_no_attributes():
    events = []
    parser('<div></div>', {
        'start': lambda t, a, u: events.append(['start', t, a, u]),
        'end': lambda t: events.append(['end', t])
    })
    assert len(events) > 1

def test_decode_attribute_values():
    atts = {}
    def set_atts(t, a, u):
        nonlocal atts
        atts = a
    parser('<a href="&lt;">', {
        'start': set_atts,
        'end': lambda *args: None
    })
    assert atts['href'] == '<'

def test_unquoted_attributes():
    atts = {}
    def set_atts(t, a, u):
        nonlocal atts
        atts = a
    parser('<a href=foo>', {
        'start': set_atts,
        'end': lambda *args: None
    })
    assert atts['href'] == 'foo'

def test_handle_boolean_attribute():
    atts = {}
    def set_atts(t, a, u):
        nonlocal atts
        atts = a
    parser('<button disabled>', {
        'start': set_atts,
        'end': lambda *args: None
    })
    assert 'disabled' not in atts or atts['disabled'] is None