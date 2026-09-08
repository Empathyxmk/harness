import os
from public_tests.helper import expect, fulfill, assert_ as assert_builtin

def test_fn_public():
    readme_file = os.path.abspath("README.markdown")
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_text = f.read()

    def fn1(name, cb):
        with open(name, 'r', encoding='utf-8') as inp:
            cb(None, inp.read())
    def fn2(err, text):
        if err:
            raise err
        return text.lower()

    pubfn = lambda name, cb: fn1(name, lambda err, text: cb(err, fn2(err, text)))

    expect('result-pub')
    def cb(err, output):
        fulfill('result-pub')
        if err:
            raise err
        assert_builtin.equal(readme_text.lower(), output, "It should transform to lower")
    pubfn(readme_file, cb)