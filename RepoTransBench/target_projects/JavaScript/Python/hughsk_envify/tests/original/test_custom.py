import io
import types
import pytest
from unittest import mock
from src.envify import custom

def simulate_stream(custom_fn, input_text):
    # Returns output text by sending to the stream and capturing output
    out = []
    stream = custom_fn()
    stream.on('data', lambda chunk: out.append(chunk))
    stream.write(input_text)
    stream.end()
    return ''.join(out)

def test_returns_transform_stream_function():
    fn = custom.custom({'FOO': 'bar'})
    assert callable(fn)

def test_handles_empty_environment():
    fn = custom.custom({})
    assert callable(fn)

def test_replaces_process_env_variables(monkeypatch):
    env = {'TEST_VAR': 'jsx'}
    stream = custom.custom(env)()
    result = []
    def on_data(chunk): result.append(chunk)
    def on_end(): 
        joined = ''.join(result)
        assert 'jsx' in joined
    stream.on('data', on_data)
    stream.on('end', on_end)
    stream.write('process.env.TEST_VAR')
    stream.end()

def test_skips_variables_not_in_env(monkeypatch):
    env = {'FOO': 'bar'}
    stream = custom.custom(env)()
    result = []
    def on_data(chunk): result.append(chunk)
    def on_end(): 
        joined = ''.join(result)
        assert 'process.env.BAZ' in joined
    stream.on('data', on_data)
    stream.on('end', on_end)
    stream.write('process.env.BAZ')
    stream.end()

def test_processes_mixed_expressions(monkeypatch):
    env = {'X': '1', 'Y': '2'}
    stream = custom.custom(env)()
    result = []
    def on_data(chunk): result.append(chunk)
    def on_end():
        joined = ''.join(result)
        assert '1' in joined
        assert '2' in joined
    stream.on('data', on_data)
    stream.on('end', on_end)
    stream.write('process.env.X + process.env.Y')
    stream.end()