"""
Legacy test.js from JS project, originally using the tape test runner.
This translation uses pytest and assumes src.envify.custom.custom(env) returns a transform stream
with .on('data', cb)/.on('end', cb), and .write/.end for input.
"""

import pytest
from src.envify import custom

class Dummy:
    pass

# Helper to run a custom stream, returning resulting buffer as a string.
def stream_result(env, input_lines, args=None):
    if args:
        stream = custom.custom(env)(__file__, args)
    else:
        stream = custom.custom(env)()
    buf = []
    stream.on('data', lambda d: buf.append(d))
    done = []
    def end_cb(): done.append('ok')
    stream.on('end', end_cb)
    stream.end('\n'.join(input_lines))
    assert done, "stream did not end"
    return ''.join(buf)

def test_replaces_environment_variables():
    buf = stream_result(
        {
            'LOREM': 'ipsum',
            'HELLO': 'world',
            'ZALGO': 'it comes'
        },
        [
            'process.env.LOREM',
            'process.env.HELLO',
            'process.env["ZALGO"]',
            'process.env[ZALGO]'
        ]
    )
    assert 'ipsum' in buf
    assert 'world' in buf
    assert 'it comes' in buf
    assert 'process.env[ZALGO]' in buf

def test_ignores_assignments():
    buf = stream_result(
        {
            'LOREM': 'ipsum',
            'HELLO': 'world',
            'UP': 'down'
        },
        [
            'process.env["LOREM"] += "lorem"',
            'process.env.LOREM += "lorem"',
            'process.env["HELLO"] = process.env["HELLO"] || "world"',
            'process.env.HELLO = process.env.HELLO || "world"',
            'process.env.UP'
        ]
    )
    assert 'world' in buf
    assert 'lorem' in buf
    assert 'process.env.LOREM' in buf
    assert 'process.env["LOREM"]' in buf
    assert 'process.env.HELLO' in buf
    assert 'process.env["HELLO"]' in buf
    assert 'down' in buf
    assert 'process.env.UP' not in buf

def test_ignores_computed_object():
    buf = stream_result(
        {
            'LOREM': 'ipsum',
            'HELLO': 'world'
        },
        [
            'process[env].LOREM',
            'process["env"].LOREM',
            'process.env.HELLO'
        ]
    )
    assert 'process[env].LOREM' in buf
    assert 'process["env"].LOREM' in buf
    assert 'process.env.HELLO' not in buf

def test_not_ignore_assigning_to_var():
    buf = stream_result(
        {
            'LOREM': 'ipsum',
            'HELLO': 'world'
        },
        [
            'var foo = process.env.LOREM',
            'oof = process.env.LOREM',
            'oof.bar = process.env.LOREM',
            'var bar = process.env.HELLO || null',
            'rab = process.env.HELLO || null',
            'a = process.env.UNDEFINED',
            'b = process.env.NOTTHERE || null'
        ]
    )
    assert 'foo = "ipsum"' in buf
    assert 'oof = "ipsum"' in buf
    assert 'oof.bar = "ipsum"' in buf
    assert 'bar = "world"' in buf
    assert 'rab = "world"' in buf
    assert 'process.env.NOTTHERE' in buf
    assert 'process.env.UNDEFINED' in buf

def test_subarg_syntax():
    buf = stream_result(
        {'OVERRIDES': 'development', 'UNTOUCHED': 'staging'},
        ['var foo = process.env.OVERRIDES', 'var bar = process.env.UNTOUCHED'],
        {'_': ['bogus', 'arguments'], 'OVERRIDES': 'production'}
    )
    assert 'foo = "production"' in buf
    assert 'bar = "staging"' in buf

def test_handles_getter_properties():
    class Env(dict):
        dyn_count = 0
        def __getitem__(self, key):
            if key == 'DYNAMIC':
                if Env.dyn_count == 0:
                    Env.dyn_count += 1
                    return 'dynamic!'
                else:
                    return 'really!'
            return dict.__getitem__(self, key)
    env = Env()
    buf = stream_result(env, [
        'var foo = process.env.DYNAMIC',
        'var bar = process.env.DYNAMIC',
    ])
    assert 'foo = "dynamic!"' in buf
    assert 'bar = "really!"' in buf

def test_envify_purge():
    args = {'_':['purge']}
    buf = stream_result({}, ['var x = process.env.PURGED'], args)
    assert 'var x = undefined' in buf
    assert 'process.env.PURGED' not in buf

def test_envify_purge_argument():
    args = {'_':['purge']}
    buf = stream_result({'argument':'not purged'}, [
        'var x = process.env.PURGED',
        'var y = process.env.argument'
    ], args)
    assert 'var x = undefined' in buf
    assert 'var y = "not purged"' in buf