from yamlmatlab import yaml
import os

def test_public_ReadYamlRaw_simpleyaml():
    r, original = yaml.ReadYamlRaw(os.path.join(
        'src',
        'yamlmatlab',
        'Data',
        'test_primitives',
        'simple.yaml'))
    assert isinstance(r, dict) and 'b' in r and isinstance(r['b'], (int, float))
    assert isinstance(original, str) and len(original) > 0

def test_public_ReadYamlRaw_utf8():
    ru, orig = yaml.ReadYamlRaw(os.path.join(
        'src',
        'yamlmatlab',
        'Data',
        'test_misc',
        'spec_chars_utf8.yaml'))
    assert isinstance(ru, dict) and 'specials' in ru
    assert isinstance(orig, str) and "ö" in orig