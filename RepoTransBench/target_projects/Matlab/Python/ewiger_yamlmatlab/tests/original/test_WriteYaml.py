import pytest
import numpy as np
from yamlmatlab import yaml
import os

def PTH_PRIMITIVES():
    return os.path.join(os.path.dirname(__file__), '../../src/yamlmatlab/Data/test_primitives/')

def PTH_IMPORT():
    return os.path.join(os.path.dirname(__file__), '../../src/yamlmatlab/Data/test_import/')

def test_WY_Matrices():
    _universal_test(PTH_PRIMITIVES(), 'matrices')

def test_WY_FloatingPoints():
    _universal_test(PTH_PRIMITIVES(), 'floating_points')

def test_WY_Indentation():
    _universal_test(PTH_PRIMITIVES(), 'indentation')

def test_WY_SequenceMapping():
    _universal_test(PTH_PRIMITIVES(), 'sequence_mapping')

def test_WY_Simple():
    _universal_test(PTH_PRIMITIVES(), 'simple')

def test_WY_Time():
    _universal_test(PTH_PRIMITIVES(), 'time')

def test_WY_ComplexStructure():
    _universal_test(PTH_IMPORT(), 'import')

def test_WY_usecase_01():
    _universal_test(PTH_PRIMITIVES(), 'usecase_struct_01')

def _universal_test(path, filename):
    import scipy.io
    mat = scipy.io.loadmat(os.path.join(path, filename + '.mat'))
    yaml.WriteYaml('~temporary.yaml', mat['testval'])
    ry = yaml.ReadYaml('~temporary.yaml')
    # For full equality, project implementation must support isequalwithequalnans logic
    assert _isequalwithequalnans(ry, mat['testval'])

def _isequalwithequalnans(a, b):
    try:
        if type(a) != type(b):
            return False
        if isinstance(a, dict):
            if set(a.keys()) != set(b.keys()):
                return False
            return all(_isequalwithequalnans(a[k], b[k]) for k in a)
        if isinstance(a, (list, tuple)):
            return len(a) == len(b) and all(_isequalwithequalnans(x, y) for x, y in zip(a, b))
        if isinstance(a, float) and isinstance(b, float):
            if np.isnan(a) and np.isnan(b):
                return True
        return a == b
    except Exception:
        return False