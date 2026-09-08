import pytest

def make_context(overrides=None):
    if overrides is None:
        overrides = {}
    return {
        'addUtilities': overrides.get('addUtilities', lambda *args, **kwargs: None),
        'e': overrides.get('e', lambda x: x),
        'theme': overrides.get('theme', lambda: {}),
    }

def fake_keyframes(context):
    add_utilities = context['addUtilities']
    e = context['e']
    theme = context['theme']()
    if not theme:
        add_utilities([])
    else:
        result = []
        for k, v in theme.items():
            result.append({'@keyframes '+e(k): v})
        add_utilities(result)

def fake_shake(context):
    add_utilities = context['addUtilities']
    shake_frames = {
        '@keyframes shake': {
            '8%, 41%': {'transform': 'translateX(-10px)'},
            '100%': {'transform': 'translateX(0)'}
        }
    }
    add_utilities(shake_frames)

def test_should_call_add_utilities_with_different_keyframes_public():
    added = []
    def add_utilities(u):
        added.extend(u)
    context = make_context({
        'addUtilities': add_utilities,
        'e': lambda x: f'escaped2-{x}',
        'theme': lambda: {'bounce': {'0%': {'opacity': .5}, '100%': {'opacity': .7}}}
    })
    fake_keyframes(context)
    assert added == [
        {'@keyframes escaped2-bounce': {'0%': {'opacity': .5}, '100%': {'opacity': .7}}}
    ]

def test_should_work_with_empty_keyframes_theme_public():
    called = {'val': False}
    def add_utilities(u):
        called['val'] = True
        assert u == []
    context = make_context({
        'addUtilities': add_utilities,
        'theme': lambda: {}
    })
    fake_keyframes(context)
    assert called['val']

def test_shake_js_should_add_shake_keyframes_public():
    called = {'val': False}
    def add_utilities(result):
        called['val'] = True
        assert '@keyframes shake' in result
        assert result['@keyframes shake']['100%']['transform'] == 'translateX(0)'
    fake_shake({'addUtilities': add_utilities})
    assert called['val']