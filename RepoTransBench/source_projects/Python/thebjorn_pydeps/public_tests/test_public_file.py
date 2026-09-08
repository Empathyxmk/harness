# -*- coding: utf-8 -*-
import os
from pydeps.py2depgraph import py2dep
from pydeps.pydeps import _pydeps
from pydeps.target import Target

from tests.filemaker import create_files
from tests.simpledeps import empty, simpledeps


def test_file_public():
    files = """
        b.py: |
            import math
    """
    with create_files(files) as workdir:
        assert simpledeps('b.py') == set()


def test_file_in_sub_directory_public():
    files = """
        baz:
            - d:
                - e.py: |
                    import f
                - f.py: ""
    """
    with create_files(files) as workdir:
        assert 'f -> e.py' in simpledeps('baz/d/e.py')


def test_file_in_directory_public():
    files = """
            - x:
                - y.py: |
                    import z
                - z.py: ""
    """
    with create_files(files) as workdir:
        assert 'z -> y.py' in simpledeps('x/y.py')


def test_file_pylib_public():
    files = """
        q.py: |
            import sys
    """
    with create_files(files) as workdir:
        assert 'sys -> q.py' in simpledeps('q.py', '--pylib')


def test_file_pyliball_public():
    files = """
        q.py: |
            import sys
    """
    with create_files(files) as workdir:
        assert 'sys -> q.py' in simpledeps('q.py', '--pylib --pylib-all')