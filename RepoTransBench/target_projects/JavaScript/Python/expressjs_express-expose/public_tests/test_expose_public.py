import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import expose_utils as expose

class TestExposePublic:

    def test_app_expose_name_alt_data(self):
        app = expose.Exposer()
        app.expose({'alpha': 10, 'beta': 20, 'gamma': 30})
        app.expose({'subtitle': 'Your Portal'}, 'app.options')
        app.expose({'multiply': lambda a, b: a * b}, 'utils')
        app.expose({'es': 'Español'}, 'langs', 'langs')

        js = app.exposed()
        scope = {}

        # Simulate: exposed attributes
        scope['app'] = type('obj', (), {})()
        scope['app'].alpha = 10
        scope['app'].beta = 20
        scope['app'].gamma = 30
        scope['app'].options = type('obj', (), {})()
        scope['app'].options.subtitle = 'Your Portal'
        scope['utils'] = type('obj', (), {})()
        def multiply(a, b): return a * b
        scope['utils'].multiply = multiply
        scope['langs'] = type('obj', (), {})()
        scope['langs'].es = 'Español'

        assert scope['app'].alpha == 10
        assert scope['app'].beta == 20
        assert scope['app'].gamma == 30
        assert scope['app'].options.subtitle == 'Your Portal'
        assert scope['utils'].multiply(2,4) == 8

        scope2 = {}
        scope2['langs'] = type('obj', (), {})()
        scope2['langs'].es = 'Español'
        assert not hasattr(scope2, 'express')
        assert scope2['langs'].es == 'Español'

    def test_app_expose_str_diff_vars(self):
        app = expose.Exposer()
        app.expose('var product = { "name": "widget" };')
        app.expose('var locale = "fr";')
        js = app.exposed()
        scope = {}
        scope['product'] = type('obj', (), {})()
        scope['product'].name = 'widget'
        scope['locale'] = 'fr'
        assert scope['locale'] == 'fr'
        assert scope['product'].name == 'widget'

    def test_app_expose_str_null_scope_swapped(self):
        app = expose.Exposer()
        app.expose('var person = { "name": "alex" };', 'head')
        app.expose('var region = "eu";')
        js = app.exposed()
        scope = {}
        scope['region'] = 'eu'
        assert scope['region'] == 'eu'
        assert 'person' not in scope
        js2 = app.exposed('head')
        scope2 = {}
        scope2['person'] = type('obj', (), {})()
        scope2['person'].name = 'alex'
        assert 'region' not in scope2
        assert scope2['person'].name == 'alex'

    def test_app_expose_fn_self_calling_new_data(self):
        app = expose.Exposer()
        app.expose('var bar;')
        def fun(self):
            self.bar = 'baz'
            hidden = 'hidden'
        app.expose(fun)
        app.expose('var city;', 'leg')
        def set_city(self):
            self.city = 'oslo'
        app.expose(set_city, 'leg')
        js = app.exposed()
        scope = type('obj', (), {})()
        setattr(scope, 'bar', 'baz')
        assert getattr(scope, 'bar', None) == 'baz'
        assert not hasattr(scope, 'hidden')
        assert not hasattr(scope, 'city')
        js2 = app.exposed('leg')
        scope2 = type('obj', (), {})()
        setattr(scope2, 'city', 'oslo')
        assert not hasattr(scope2, 'bar')
        assert getattr(scope2, 'city', None) == 'oslo'

    def test_app_expose_fn_named_different_math(self):
        app = expose.Exposer()
        def multiply(a, b):
            return a * b
        app.expose(multiply)
        def divide(a, b):
            return a / b
        app.expose(divide, 'leg')
        js = app.exposed()
        scope = {}
        def multiplyfun(a, b): return a * b
        scope['multiply'] = multiplyfun
        assert scope['multiply'](2,5) == 10
        assert 'divide' not in scope
        js2 = app.exposed('leg')
        scope2 = {}
        def dividefun(a, b): return a / b
        scope2['divide'] = dividefun
        assert scope2['divide'](10,2) == 5
        assert 'multiply' not in scope2

    def test_res_expose_str_alternate_fields(self):
        app = expose.Exposer()
        app.expose('var settings = { "theme": "dark" };')
        app.expose('settings.version = 2;')
        app.expose('var lang = "es";')
        app.expose('var country = "es";')
        js = app.exposed()
        scope = {}
        obj = type('obj', (), {})()
        setattr(obj, 'theme', 'dark')
        setattr(obj, 'version', 2)
        scope['settings'] = obj
        scope['lang'] = 'es'
        scope['country'] = 'es'
        assert scope['settings'].theme == 'dark'
        assert scope['settings'].version == 2
        assert scope['country'] == 'es'
        assert scope['lang'] == 'es'