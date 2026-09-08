import os
import numpy as np
from yamlmatlab import yaml

def PTH_PRIMITIVES():
    return os.path.join(os.path.dirname(__file__), '../src/yamlmatlab/Data/test_primitives/')

def PTH_IMPORT():
    return os.path.join(os.path.dirname(__file__), '../src/yamlmatlab/Data/test_import/')

def test_WY_Indentation():
    _public_universal(PTH_PRIMITIVES(), 'indentation')

def test_WY_Matrices():
    _public_universal(PTH_PRIMITIVES(), 'matrices')

def test_WY_FloatingPoints():
    _public_universal(PTH_PRIMITIVES(), 'floating_points')

def test_WY_SequenceMapping():
    _public_universal(PTH_PRIMITIVES(), 'simple')

def test_WY_Simple():
    _public_universal(PTH_PRIMITIVES(), 'sequence_mapping')

def test_WY_Time():
    _public_universal(PTH_PRIMITIVES(), 'usecase_struct_01')

def test_WY_ComplexStructure():
    _public_universal(PTH_IMPORT(), 'import_def')

def test_WY_usecase_01():
    _public_universal(PTH_PRIMITIVES(), 'time_variants')

def _public_universal(path, filename):
    import scipy.io
    mat = scipy.io.loadmat(os.path.join(path, filename + '.mat'))
    yaml.WriteYaml('~public_temporary.yaml', mat['testval'])
    ry = yaml.ReadYaml('~public_temporary.yaml')
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