from tests.helper import expect, fulfill
from tests.helper import assert_ as assert_builtin
import os

def Step_fn(fn1, fn2):
    def wrapped(*args):
        def cb(err, result):
            fn2(err, result)
        fn1(args[0], cb)
    return wrapped

def test_fn_transform(tmp_path):
    THIS_FILE = os.path.abspath(__file__)
    with open(THIS_FILE, "r", encoding='utf-8') as f:
        self_text = f.read()

    def fn1(name, cb):
        with open(name, 'r', encoding='utf-8') as inp:
            cb(None, inp.read())

    def fn2(err, text):
        if err:
            raise err
        return text.upper()

    myfn = Step_fn(fn1, fn2)

    expect('result')

    def cb(err, result):
        fulfill('result')
        if err:
            raise err
        assert_builtin.equal(self_text.upper(), result, "It should work")

    myfn(THIS_FILE, cb)