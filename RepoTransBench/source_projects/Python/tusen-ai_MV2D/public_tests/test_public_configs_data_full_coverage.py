import importlib.util
import os
import pytest

DATA_FILES = [
    "configs/mv2d/data/two_frames.py",   # different from original which uses single_frame
]

@pytest.mark.parametrize("data_path", DATA_FILES)
def test_public_data_config_keys_and_types(data_path):
    cfg_path = os.path.abspath(data_path)
    spec = importlib.util.spec_from_file_location("public_test_data", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # "class_names" must be present and non-empty
    assert hasattr(module, "class_names")
    assert isinstance(module.class_names, (list, tuple))
    assert len(module.class_names) > 0
    # "train_pipeline" must be a list of dict(s)
    assert hasattr(module, "train_pipeline")
    assert isinstance(module.train_pipeline, list)
    assert all(isinstance(x, dict) for x in module.train_pipeline)
    # "test_pipeline" must be present and be a list
    assert hasattr(module, "test_pipeline")
    assert isinstance(module.test_pipeline, list)
    # "data" must exist and be a dict with "train", "val" at least
    assert hasattr(module, "data")
    assert isinstance(module.data, dict)
    for key in ("train", "val"):
        assert key in module.data

@pytest.mark.parametrize("data_path", DATA_FILES)
def test_public_point_cloud_range_variety(data_path):
    cfg_path = os.path.abspath(data_path)
    spec = importlib.util.spec_from_file_location("public_test_data2", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # The public test will assert its point_cloud_range is different in some way (to enforce diff)
    assert hasattr(module, "point_cloud_range")
    pcr = module.point_cloud_range
    assert isinstance(pcr, (list, tuple))
    # Enforce that ranges have some < 0 and some > 0 values (test variety)
    assert any(x < 0 for x in pcr) and any(x > 0 for x in pcr)