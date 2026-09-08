import pytest
from src.envify import custom

def test_returns_transform_stream_function_with_alt_env():
    fn = custom.custom({'BAR': 'baz'})
    assert callable(fn)

def test_handles_completely_empty_env():
    fn = custom.custom(type('EmptyObj', (), {})())
    assert callable(fn)

def test_replaces_process_env_variables_in_alternate_source():
    env = {'ALT_VAR': 'qux'}
    stream = custom.custom(env)()
    result = []
    def on_data(chunk): result.append(chunk)
    def on_end():
        joined = ''.join(result)
        assert 'qux' in joined
    stream.on('data', on_data)
    stream.on('end', on_end)
    stream.write('process.env.ALT_VAR')
    stream.end()

def test_leaves_untouched_variables_not_in_env():
    env = {'ALPHA': 'omega'}
    stream = custom.custom(env)()
    result = []
    def on_data(chunk): result.append(chunk)
    def on_end():
        joined = ''.join(result)
        assert 'process.env.BETA' in joined
    stream.on('data', on_data)
    stream.on('end', on_end)
    stream.write('process.env.BETA')
    stream.end()

def test_processes_multiple_mixed_env_expressions():
    env = {'FOO1': 'apple', 'FOO2': 'orange'}
    stream = custom.custom(env)()
    result = []
    def on_data(chunk): result.append(chunk)
    def on_end():
        joined = ''.join(result)
        assert 'apple' in joined
        assert 'orange' in joined
    stream.on('data', on_data)
    stream.on('end', on_end)
    stream.write('process.env.FOO1 + process.env.FOO2')
    stream.end()