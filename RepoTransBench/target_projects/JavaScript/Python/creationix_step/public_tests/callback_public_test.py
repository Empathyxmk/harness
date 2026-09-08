import os
from public_tests.helper import expect, fulfill, assert_ as assert_builtin

def test_callback_public():
    license_file = os.path.abspath("license.txt")
    with open(license_file, 'r', encoding='utf-8') as f:
        license_text = f.read()

    expect('uno')
    expect('dos')
    expect('tres')

    def read_license(cb):
        fulfill("uno")
        with open(license_file, 'r', encoding='utf-8') as lf:
            cb(None, lf.read())
    def capitalize(err, text, cb):
        fulfill("dos")
        if err:
            raise err
        assert_builtin.equal(license_text, text, "License Text Loaded")
        return text[::-1]
    def show_it(err, new_text, cb):
        fulfill("tres")
        if err:
            raise err
        assert_builtin.equal(license_text[::-1], new_text, "License Text Reversed")

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

    Step(read_license, capitalize, show_it)