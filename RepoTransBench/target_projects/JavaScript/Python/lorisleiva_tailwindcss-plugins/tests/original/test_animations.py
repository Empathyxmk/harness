import pytest

def make_context(overrides=None):
    if overrides is None:
        overrides = {}
    return {
        'addUtilities': overrides.get('addUtilities', lambda *args, **kwargs: None),
        'e': overrides.get('e', lambda x: x),
        'theme': overrides.get('theme', lambda: {}),
        'variants': overrides.get('variants', lambda: []),
    }

def fake_animations(context):
    add_utilities = context['addUtilities']
    e = context['e']
    theme = context['theme']()
    variants = context['variants']()
    if not theme:
        add_utilities([], [])
    else:
        result = []
        for name, value in theme.items():
            result.append({f'.{e(name)}': {'animation': value}})
        add_utilities(result, variants)

def test_should_call_add_utilities_with_correct_utilities_and_variants():
    added = {}
    def add_utilities(u, v):
        added['u'] = u
        added['v'] = v
    context = make_context({
        'addUtilities': add_utilities,
        'e': lambda x: f'escaped-{x}',
        'theme': lambda: {'bounce': 'bounce 1s infinite'},
        'variants': lambda: ['responsive']
    })
    fake_animations(context)
    assert added['u'] == [
        {'.escaped-bounce': {'animation': 'bounce 1s infinite'}}
    ]
    assert added['v'] == ['responsive']

def test_should_work_with_empty_animations_theme():
    called = {'val': False}
    def add_utilities(u, v):
        called['val'] = True
        assert u == []
        assert v == []
    context = make_context({
        'addUtilities': add_utilities,
        'theme': lambda: {},
        'variants': lambda: [],
    })
    fake_animations(context)
    assert called['val']