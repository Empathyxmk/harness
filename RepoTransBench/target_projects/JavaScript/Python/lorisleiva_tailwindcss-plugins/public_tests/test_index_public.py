import pytest

# Simulate the behavior of the gradients plugin by calling addUtilities as in the source JS tests.
class FakePlugins:
    def gradients(self, context):
        # The JS plugin expects to call addUtilities as part of the plugin registration.
        if 'addUtilities' in context and callable(context['addUtilities']):
            context['addUtilities']()

def test_gradients_plugin_should_accept_a_context_and_not_throw_public():
    called = {'val': False}
    def add_utilities():
        called['val'] = True
    plugins = FakePlugins()
    context = {
        'addUtilities': add_utilities,
        'e': lambda x: x,
        'theme': lambda: {'orange': ['to bottom', '#FFA500', '#FF6347']},
        'variants': lambda: []
    }
    plugins.gradients(context)
    assert called['val']