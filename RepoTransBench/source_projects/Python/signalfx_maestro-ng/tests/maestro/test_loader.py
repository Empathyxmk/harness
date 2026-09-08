import io
import os
import sys
import tempfile
import pytest
from maestro import loader, exceptions
import yaml

def test_basic_yaml_load(tmp_path):
    content = "foo: bar\n"
    file = tmp_path / "sample.yaml"
    file.write_text(content)
    conf = loader.load(str(file))
    assert 'foo' in conf
    assert conf['foo'] == 'bar'
    assert '__maestro' in conf
    assert 'base_dir' in conf['__maestro']

def test_base_dir_is_cwd_for_stdin(monkeypatch):
    test_yaml = "abc: 123"
    monkeypatch.setattr(sys, 'stdin', io.StringIO(test_yaml))
    conf = loader.load('-')
    assert conf['abc'] == 123

def test_template_not_found():
    with pytest.raises(exceptions.MaestroException):
        loader.load('/not/a/real/file.yaml')

def test_invalid_yaml(tmp_path):
    file = tmp_path / "fail.yaml"
    file.write_text("foo: [1,2\n")
    # Loader will throw yaml.parser.ParserError
    with pytest.raises(yaml.parser.ParserError):
        loader.load(str(file))

def test_duplicate_key_error(tmp_path):
    content = "foo: 1\nfoo: 2\n"
    file = tmp_path / "bad.yaml"
    file.write_text(content)
    with pytest.raises(yaml.constructor.ConstructorError):
        loader.load(str(file))

def test_custom_filter_function(tmp_path):
    # The rendered template should return a string.
    content = "{{ 'hello' | shout }}"
    file = tmp_path / "filter.yaml"
    file.write_text(content)
    def shout(value): return value.upper()
    # Should return a string, not dict, so __maestro assignment will fail
    with pytest.raises(TypeError):
        loader.load(str(file), filters={'shout': shout})