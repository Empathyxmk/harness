import os
from yamlmatlab import yaml

def test_public_doinheritance_multiple():
    s = yaml.doinheritance(
        os.path.join(
            'src',
            'yamlmatlab',
            'Data',
            'test_inheritance',
            'inheritance_multiple.yaml')
    )
    assert 'bar' in s and 'baz' in s
    assert s['baz'] == 22

def test_public_doinheritance_loop_detect():
    caught = False
    try:
        yaml.doinheritance(
            os.path.join(
                'src',
                'yamlmatlab',
                'Data',
                'test_inheritance',
                'inheritance_loop.yaml')
        )
    except Exception:
        caught = True
    assert caught, 'Did not catch loop in inheritance as expected'