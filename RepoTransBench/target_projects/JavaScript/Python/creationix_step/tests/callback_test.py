import os
import pytest

from tests.helper import expect, fulfill
from tests.helper import assert_ as assert_builtin

def read_file(filename, mode, cb):
    with open(filename, mode) as f:
        cb(None, f.read())

def Step(*funcs):
    queue = list(funcs)
    def callback(*args):
        if not queue:
            if args and args[0]:
                raise args[0]
            return
        func = queue.pop(0)
        try:
            if len(args) == 0:
                result = func(callback)
            else:
                result = func(*args, callback)
            if result is not None:
                callback(None, result)
        except Exception as e:
            callback(e)
    callback()

def test_callback_async_and_sync(tmp_path):
    THIS_FILE = os.path.abspath(__file__)
    with open(THIS_FILE, 'r', encoding='utf-8') as f:
        self_text = f.read()

    steps = []

    expect('one')
    expect('two')
    expect('three')

    def read_self(cb):
        fulfill('one')
        read_file(THIS_FILE, 'r', cb)
    def capitalize(err, text, cb):
        fulfill('two')
        if err:
            raise err
        assert_builtin.equal(self_text, text, "Text Loaded")
        return text.upper()
    def show_it(err, new_text, cb):
        fulfill('three')
        if err:
            raise err
        assert_builtin.equal(self_text.upper(), new_text, "Text Uppercased")

    Step(read_self, capitalize, show_it)