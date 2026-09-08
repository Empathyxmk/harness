import pytest
from benface_tailwindcss_transforms.index import transforms_plugin

class DummyMockApi:
    def __init__(self):
        self.addUtilities = self._spy('addUtilities')
        self.addComponents = self._spy('addComponents')
        self.theme = self._theme
        self.e = lambda x: x
        self.variants = self._variants

    def _spy(self, name):
        calls = []
        def fn(*args, **kwargs):
            calls.append((args, kwargs))
        fn.calls = calls
        fn.called = lambda : len(calls) > 0
        fn.call_args = lambda idx=0: (calls[idx][0], calls[idx][1]) if len(calls) > idx else (None, None)
        return fn

    def _theme(self, type_):
        presets = {
            "translate": {0: '0', 1: '0.25rem'},
            "scale": {0: '0', 1: '1'},
            "rotate": {0: '0', 45: '45deg'},
            "skew": {0: '0', 12: '12deg'},
            "transformOrigin": {'center': 'center', 'top': 'top', 'left': 'left'}
        }
        return presets.get(type_, {})

    def _variants(self, utility):
        return ['responsive', 'hover']

def test_should_call_add_utilities_and_add_components_when_run():
    api = DummyMockApi()
    transforms_plugin(api)
    assert api.addUtilities.called()
    assert api.addComponents.called()

def test_should_use_default_options_when_none_are_provided():
    api = DummyMockApi()
    transforms_plugin(api)
    calls, _ = api.addUtilities.call_args(0)
    # The dict as first posarg
    assert '.transform-none' in calls[0]

def test_should_respect_custom_config():
    api = DummyMockApi()
    config = {"respectImportant": True}
    transforms_plugin(api, config)
    assert api.addUtilities.called()

def test_should_handle_absence_of_theme_variants_gracefully():
    class ShortApi:
        def __init__(self):
            self.addUtilities = lambda *args, **kw: self._called_util(args)
            self.addComponents = lambda *args, **kw: self._called_comp(args)
            self.variants = lambda *args, **kw: []
            self.theme = lambda *args, **kw: {}
            self.e = lambda x: x
            self._util_calls = []
            self._comp_calls = []
        def _called_util(self, args):
            self._util_calls.append(args)
        def _called_comp(self, args):
            self._comp_calls.append(args)
    api = ShortApi()
    # Should not raise
    transforms_plugin(api)