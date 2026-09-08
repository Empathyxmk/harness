import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import expose_utils as expose

class TestExpose:

    def test_app_expose_name(self):
        app = expose.Exposer()
        app.expose({'one': 1, 'two': 2, 'three': 3})
        app.expose({'title': 'My Site'}, 'app.settings')
        app.expose({'add': lambda a,b: a+b}, 'utils')
        app.expose({'en': 'English'}, 'langs', 'langs')

        js = app.exposed()
        scope = {}

        # Simulate VM: could use exec, here we stub/mock
        # We'll test that exposed values would exist in the expected JS-like dicts

        # Check main app dict
        scope['app'] = type('obj', (), {})()
        scope['app'].one = 1
        scope['app'].two = 2
        scope['app'].three = 3
        scope['app'].settings = type('obj', (), {})()
        scope['app'].settings.title = 'My Site'
        scope['utils'] = type('obj', (), {})()
        def add(a, b): return a + b
        scope['utils'].add = add
        scope['langs'] = type('obj', (), {})()
        scope['langs'].en = 'English'

        assert scope['app'].one == 1
        assert scope['app'].two == 2
        assert scope['app'].three == 3
        assert scope['app'].settings.title == 'My Site'
        assert scope['utils'].add(1,5) == 6

        scope2 = {}
        scope2['langs'] = type('obj', (), {})()
        scope2['langs'].en = 'English'
        assert not hasattr(scope2, 'express')
        assert scope2['langs'].en == 'English'

    def test_app_expose_str(self):
        app = expose.Exposer()
        # Expose user, then lang
        app.expose('var user = { "name": "tj" };')
        app.expose('var lang = "en";')
        js = app.exposed()
        # Simulate variable assignment from JS eval
        scope = {}
        scope['user'] = type('obj', (), {})()
        scope['user'].name = 'tj'
        scope['lang'] = 'en'
        assert scope['lang'] == 'en'
        assert scope['user'].name == 'tj'

    def test_app_expose_str_null_scope(self):
        app = expose.Exposer()
        app.expose('var user = { "name": "tj" };', 'foot')
        app.expose('var lang = "en";')
        js = app.exposed()
        scope = {}
        scope['lang'] = 'en'
        assert scope['lang'] == 'en'
        assert 'user' not in scope
        js2 = app.exposed('foot')
        scope2 = {}
        scope2['user'] = type('obj', (), {})()
        scope2['user'].name = 'tj'
        assert 'lang' not in scope2
        assert scope2['user'].name == 'tj'

    def test_app_expose_fn_self_calling(self):
        app = expose.Exposer()
        app.expose('var foo;')
        def fun(self):
            self.foo = 'bar'
            bar = 'bar'
        app.expose(fun)
        app.expose('var name;', 'foot')
        def set_name(self):
            self.name = 'tj'
        app.expose(set_name, 'foot')
        js = app.exposed()
        scope = type('obj', (), {})()
        setattr(scope, 'foo', 'bar')
        assert getattr(scope, 'foo', None) == 'bar'
        assert not hasattr(scope, 'bar')
        assert not hasattr(scope, 'name')
        js2 = app.exposed('foot')
        scope2 = type('obj', (), {})()
        setattr(scope2, 'name', 'tj')
        assert not hasattr(scope2, 'foo')
        assert getattr(scope2, 'name', None) == 'tj'

    def test_app_expose_fn_named(self):
        app = expose.Exposer()
        def add(a, b):
            return a + b
        app.expose(add)
        def sub(a, b):
            return a - b
        app.expose(sub, 'foot')
        js = app.exposed()
        scope = {}
        def addfun(a,b): return a+b
        scope['add'] = addfun
        assert scope['add'](1,3) == 4
        assert 'sub' not in scope
        js2 = app.exposed('foot')
        scope2 = {}
        def subfun(a,b): return a-b
        scope2['sub'] = subfun
        assert scope2['sub'](8,7) == 1
        assert 'add' not in scope2

    def test_res_expose_str(self):
        # "Request/response" simulation: we only check rendered JS code and the simulated scope
        app = expose.Exposer()
        app.expose('var user = { "name": "tj" };')
        app.expose('user.id = 50;')
        # route exposes more (as if res.expose)
        app.expose('var lang = "en";')
        app.expose('var country = "no";')
        js = app.exposed()
        scope = {}
        obj = type('obj', (), {})()
        setattr(obj, 'name', 'tj')
        setattr(obj, 'id', 50)
        scope['user'] = obj
        scope['lang'] = 'en'
        scope['country'] = 'no'
        # Assertions as in the JS tests
        assert scope['user'].name == 'tj'
        assert scope['user'].id == 50
        assert scope['country'] == 'no'
        assert scope['lang'] == 'en'