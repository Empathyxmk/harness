# -*- coding: utf-8 -*-
from pydeps.pydeps import pydeps
from tests.filemaker import create_files
from tests.simpledeps import simpledeps


def test_from_customlib_public():
    files = """
        zoo:
            - __init__.py
            - tiger.py: |
                from custom import py
        custom:
            - __init__.py
            - py.py: |
                somevar = 100
    """
    with create_files(files) as workdir:
        assert simpledeps('zoo', '--show-deps -LINFO -vv') == {
            'custom -> zoo.tiger',
            'custom.py -> zoo.tiger'
        }


def test_multidot_public():
    files = """
        alpha.beta.py: |
            from random import randint
    """
    with create_files(files) as workdir:
        assert simpledeps('alpha.beta.py', '--show-deps --pylib -LINFO -vv') == {
            'random -> alpha.beta.py',
        }