# -*- coding: utf-8 -*-
import json
import os
from pydeps import pydeps
from tests.filemaker import create_files
from tests.simpledeps import simpledeps, depgrf


def test_dep2dot_public():
    files = """
        bar:
            - __init__.py
            - x.py: |
                from . import y
            - y.py
    """
    with create_files(files) as workdir:
        g = depgrf("bar")
        d = json.loads(repr(g))
        print(d)
        assert '__main__' in d['bar']['imported_by']
        assert g.sources['bar.x'] == g.sources['bar.x']
        assert str(g.sources['bar.x']).startswith('bar.x')
        assert 'bar.y' in repr(g.sources['bar.x'])