import io
import types
import pytest
from yacs.config import CfgNode as CN

def test_load_cfg_yaml_and_py(tmp_path):
    # YAML file test - different content
    yaml_content = """
    K: 789
    L:
      M: false
    """
    yaml_file = tmp_path / "test_diff.yaml"
    yaml_file.write_text(yaml_content)
    cfg = CN(new_allowed=True)
    cfg.merge_from_file(str(yaml_file))
    assert cfg.K == 789
    assert cfg.L.M is False

    # Python file test (must define variable 'cfg' at top-level!)
    py_content = "cfg = dict(Z=[7,8,9], Y=dict(X='baz'))"
    py_file = tmp_path / "f2.py"
    py_file.write_text(py_content)
    cfg2 = CN(new_allowed=True)
    cfg2.merge_from_file(str(py_file))
    assert cfg2.Z == [7, 8, 9]
    assert cfg2.Y.X == 'baz'

def test_load_cfg_file_object_yaml():
    yaml_str = "A: 88\nB: [4, 5, 6]"
    fobj = io.StringIO(yaml_str)
    import yaml
    dct = yaml.safe_load(fobj)
    cfg = CN(new_allowed=True)
    cfg.merge_from_other_cfg(CN(dct, new_allowed=True))
    assert cfg.A == 88
    assert cfg.B == [4, 5, 6]

def test_load_cfg_file_object_py(tmp_path):
    py_content = "ALPHA = [100,200,300]"
    py_file = tmp_path / "f_obj.py"
    py_file.write_text(py_content)
    code = compile(py_file.read_text(), str(py_file), "exec")
    mod = types.ModuleType("cfg_temp")
    exec(code, mod.__dict__)
    cfg_dict = {k: v for k, v in mod.__dict__.items() if not k.startswith("__")}
    cfg = CN(cfg_dict, new_allowed=True)
    assert cfg.ALPHA == [100, 200, 300]

def test_dump_and_load_roundtrip(tmp_path):
    cfg = CN({'foo': 21, 'bar': "hello world"})
    text = cfg.dump()
    dumped_file = tmp_path / "public_dumped.yaml"
    dumped_file.write_text(text)
    new_cfg = CN(new_allowed=True)
    new_cfg.merge_from_file(str(dumped_file))
    assert new_cfg.foo == 21
    assert new_cfg.bar == "hello world"

def test_wrong_extension(tmp_path):
    file_path = tmp_path / "bad2.txt"
    file_path.write_text("BAR=3")
    with pytest.raises(Exception):
        CN.load_cfg(str(file_path))