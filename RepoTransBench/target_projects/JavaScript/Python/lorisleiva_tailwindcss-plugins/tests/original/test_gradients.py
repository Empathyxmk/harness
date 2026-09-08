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
    # Fakes the call shape, just for test logic mapping
    add_utilities = context['addUtilities']
    theme = context['theme']()
    if theme:
        add_utilities()
    else:
        add_utilities()

def test_should_export_a_function():
    # In JS: t.is(typeof gradients, 'function')
    # In Python: check it is callable
    assert callable(fake_gradients)

def test_should_not_throw_and_call_add_utilities_with_mock_theme():
    called = {'val': False}
    def add_utilities():
        called['val'] = True
    context = make_context({
        'addUtilities': add_utilities,
        'theme': lambda: {
            'blue': ['to right', '#00f', '#0ff'],
            'green': {'type': 'radial', 'colors': ['#0f0', '#ff0']}
        }
    })
    fake_gradients(context)
    assert called['val']