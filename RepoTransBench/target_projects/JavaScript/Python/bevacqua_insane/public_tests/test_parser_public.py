import pytest

try:
    from src.parser import parser
except ImportError:
    import sys
    parser = sys.modules.get('parser', None)

def test_parse_simple_single_tag():
    html = '<h1>Hello</h1>'
    events = []
    parser(html, {
        'start': lambda tag, attrs, unary: events.append(f"start:{tag}"),
        'end': lambda tag: events.append(f"end:{tag}"),
        'chars': lambda text: events.append(f"text:{text}"),
        'comment': lambda text: events.append(f"comment:{text}")
    })
    assert events == ['start:h1', 'text:Hello', 'end:h1']

def test_parse_nested_tags_and_text():
    html = '<div><span>Nice!</span>Text</div>'
    out = []
    parser(html, {
        'start': lambda tag, attrs, unary: out.append(f"<{tag}>"),
        'end': lambda tag: out.append(f"</{tag}>"),
        'chars': lambda text: out.append(text)
    })
    assert out == ['<div>', '<span>', 'Nice!', '</span>', 'Text', '</div>']

def test_trigger_comment_callback_for_html_comments():
    html = '<div><!--something--></div>'
    events = []
    parser(html, {
        'start': lambda tag, attrs, unary: events.append(f"S:{tag}"),
        'end': lambda tag: events.append(f"E:{tag}"),
        'chars': lambda *a, **kw: None,
        'comment': lambda text: events.append(f"C:{text}")
    })
    assert events == ['S:div', 'C:something', 'E:div']