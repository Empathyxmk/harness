from benface_tailwindcss_transforms.index import transforms_plugin

class CustomMockApi:
    def __init__(self):
        self.addUtilities = self._spy('addUtilities')
        self.addComponents = self._spy('addComponents')
        self.theme = self._theme
        self.e = lambda x: f"escape__{x}"
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
        customPresets = {
            "translate": {2: "0.5rem", 3: "0.75rem"},
            "scale": {2: "2", 3: "3"},
            "rotate": {90: "90deg", 180: "180deg"},
            "skew": {27: "27deg", 45: "45deg"},
            "transformOrigin": {"bottom": "bottom", "right": "right", "center": "center"}
        }
        return customPresets.get(type_, {})

    def _variants(self, utility):
        return ['focus', 'active']

def test_should_call_add_utilities_and_add_components_for_different_config():
    api = CustomMockApi()
    transforms_plugin(api)
    assert api.addUtilities.called()
    assert api.addComponents.called()

def test_should_use_custom_options_and_handle_keys():
    api = CustomMockApi()
    transforms_plugin(api)
    calls, _ = api.addUtilities.call_args(0)
    added_keys = list(calls[0].keys())
    assert '.transform-none' in added_keys
    assert '.translate-x-2' in added_keys
    assert '.translate-y-3' in added_keys

def test_should_respect_a_new_config_option():
    api = CustomMockApi()
    config = {"crazyOption": False}
    transforms_plugin(api, config)
    assert api.addUtilities.called()

def test_should_handle_absence_of_theme_variants_gracefully_on_different_mock():
    class ShortApi:
        def __init__(self):
            self.addUtilities = lambda *args, **kw: self._util_called(args)
            self.addComponents = lambda *args, **kw: self._comp_called(args)
            self.variants = lambda *args, **kw: []
            self.theme = lambda *args, **kw: {}
            self.e = lambda x: x
            self._util_calls = []
            self._comp_calls = []
        def _util_called(self, args):
            self._util_calls.append(args)
        def _comp_called(self, args):
            self._comp_calls.append(args)
    api = ShortApi()
    # Should not raise
    transforms_plugin(api)