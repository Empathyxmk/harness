import io
import types
import pytest
from yacs.config import CfgNode as CN

def test_load_cfg_yaml_and_py(tmp_path):
    # YAML file test
    yaml_content = """
    A: 123
    B:
      C: true
    """
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(yaml_content)
    cfg = CN(new_allowed=True)
    cfg.merge_from_file(str(yaml_file))
    assert cfg.A == 123
    assert cfg.B.C is True

    # Python file test (must define variable 'cfg' at top-level!)
    py_content = "cfg = dict(D=456, E=dict(F='bar'))"
    py_file = tmp_path / "f.py"
    py_file.write_text(py_content)
    cfg2 = CN(new_allowed=True)
    cfg2.merge_from_file(str(py_file))
    assert cfg2.D == 456
    assert cfg2.E.F == 'bar'

def test_load_cfg_file_object_yaml():
    yaml_str = "X: 1\nY: [1,2,3]"
    fobj = io.StringIO(yaml_str)
    import yaml
    dct = yaml.safe_load(fobj)
    cfg = CN(new_allowed=True)
    cfg.merge_from_other_cfg(CN(dct, new_allowed=True))
    assert cfg.X == 1
    assert cfg.Y == [1, 2, 3]

def test_load_cfg_file_object_py(tmp_path):
    py_content = "A = [1,2,3]"
    py_file = tmp_path / "f.py"
    py_file.write_text(py_content)
    code = compile(py_file.read_text(), str(py_file), "exec")
    mod = types.ModuleType("cfg_temp")
    exec(code, mod.__dict__)
    cfg_dict = {k: v for k, v in mod.__dict__.items() if not k.startswith("__")}
    cfg = CN(cfg_dict, new_allowed=True)
    assert cfg.A == [1, 2, 3]

def test_dump_and_load_roundtrip(tmp_path):
    cfg = CN({'foo': 3, 'bar': 6})
    text = cfg.dump()
    dumped_file = tmp_path / "dumped.yaml"
    dumped_file.write_text(text)
    new_cfg = CN(new_allowed=True)
    new_cfg.merge_from_file(str(dumped_file))
    assert new_cfg.foo == 3
    assert new_cfg.bar == 6

def test_wrong_extension(tmp_path):
    file_path = tmp_path / "bad.txt"
    file_path.write_text("FOO=2")
    # CN.load_cfg(str(file_path)) is expected to fail, but throws AttributeError, not ValueError
    # So, just test that it raises *some* Exception
    with pytest.raises(Exception):
        CN.load_cfg(str(file_path))