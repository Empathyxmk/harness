from yamlmatlab import yaml
import os

def test_public_ReadYaml_misc_file():
    out = yaml.ReadYaml(os.path.join(
        'src',
        'yamlmatlab',
        'Data',
        'test_misc',
        'dos_CRLF.yaml'
    ))
    assert 'somefield' in out and 'subfield' in out['somefield']
    assert out['somefield']['subfield'] == 'with crlf'

def test_public_ReadYaml_whitespace_file():
    out = yaml.ReadYaml(os.path.join(
        'src',
        'yamlmatlab',
        'Data',
        'test_primitives',
        'whitespaces.yaml'
    ))
    assert isinstance(out, dict)
    assert 'with_spaces' in out