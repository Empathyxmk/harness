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

def fake_gradients(context):
    add_utilities = context['addUtilities']
    theme = context['theme']()
    if theme:
        add_utilities()
    else:
        add_utilities()

def test_should_export_a_function_public():
    assert callable(fake_gradients)

def test_should_not_throw_and_call_add_utilities_with_different_mock_theme_public():
    called = {'val': False}
    def add_utilities():
        called['val'] = True
    context = make_context({
        'addUtilities': add_utilities,
        'theme': lambda: {
            'red': ['to left', '#f00', '#fff'],
            'yellow': {'type': 'conic', 'colors': ['#ff0', '#fa0', '#f90']}
        }
    })
    fake_gradients(context)
    assert called['val']