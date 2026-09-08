import pytest
import os
from yamlmatlab import yaml

def PTH_PRIMITIVES():
    return os.path.join(os.path.dirname(__file__), '../../src/yamlmatlab/Data/test_primitives/')

def PTH_IMPORT():
    return os.path.join(os.path.dirname(__file__), '../../src/yamlmatlab/Data/test_import/')

def PTH_INHERITANCE():
    return os.path.join(os.path.dirname(__file__), '../../src/yamlmatlab/Data/test_inheritance/')

def test_RY_Matrices():
    _read_compare(PTH_PRIMITIVES(), 'matrices')

def test_RY_Whitespaces():
    ry = yaml.ReadYaml(os.path.join(PTH_PRIMITIVES(), 'whitespaces.yaml'))
    assert 'ImageFile' in ry and 'ContoursCount' in ry

def test_RY_FloatingPoints():
    _read_compare_nan(PTH_PRIMITIVES(), 'floating_points')

def test_RY_Indentation():
    _read_compare(PTH_PRIMITIVES(), 'indentation')

def test_RY_SequenceMapping():
    _read_compare(PTH_PRIMITIVES(), 'sequence_mapping')

def test_RY_Simple():
    _read_compare(PTH_PRIMITIVES(), 'simple')

def test_RY_Time():
    _read_compare(PTH_PRIMITIVES(), 'time')

def test_RY_TimeVariants():
    _read_compare_nan(PTH_PRIMITIVES(), 'time_variants')

def test_RY_Import():
    _read_compare(PTH_IMPORT(), 'import')

def test_RY_ImportDef():
    _read_compare(PTH_IMPORT(), 'import_def')

def test_RY_ImportNonex():
    import pytest
    fname = os.path.join(PTH_IMPORT(), 'import_nonex.yaml')
    with pytest.raises(FileNotFoundError) as e:
        yaml.ReadYaml(fname, 1)

def test_RY_Inheritance():
    _read_compare(PTH_INHERITANCE(), 'inheritance')

def test_RY_InheritanceMultiple():
    _read_compare(PTH_INHERITANCE(), 'inheritance_multiple')

def test_RY_InheritanceLoop():
    import pytest
    fname = os.path.join(PTH_INHERITANCE(), 'inheritance_loop.yaml')
    with pytest.raises(RuntimeError):
        yaml.ReadYaml(fname)

def test_RY_usecase_01():
    _read_compare_nan(PTH_PRIMITIVES(), 'usecase_struct_01')

def _read_compare(base, file):
    import scipy.io
    yaml_file = os.path.join(base, file+'.yaml')
    mat = scipy.io.loadmat(os.path.join(base, file+'.mat'))
    ry = yaml.ReadYaml(yaml_file)
    assert ry == mat['testval']

def _read_compare_nan(base, file):
    import numpy as np
    import scipy.io
    yaml_file = os.path.join(base, file+'.yaml')
    mat = scipy.io.loadmat(os.path.join(base, file+'.mat'))
    ry = yaml.ReadYaml(yaml_file)
    # isequalwithequalnans logic:
    assert _isequalwithequalnans(ry, mat['testval'])

def _isequalwithequalnans(a, b):
    import numpy as np
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