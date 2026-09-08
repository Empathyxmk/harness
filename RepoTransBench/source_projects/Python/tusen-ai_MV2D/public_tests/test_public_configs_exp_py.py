import importlib.util
import os

def test_public_configs_exp_py_importable():
    # Use two different exp configs (not in the same set as those in original test)
    config_paths = [
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py"
    ]
    for path in config_paths:
        cfg_path = os.path.abspath(path)
        spec = importlib.util.spec_from_file_location(f"cfg_{os.path.basename(path)}", cfg_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, "model")
        assert isinstance(module.model, dict)
        assert hasattr(module, "point_cloud_range")
        assert hasattr(module, "roi_size")

def test_public_configs_exp_py_roi_stride():
    # Use only one variant, but different data file from existing test
    path = "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py"
    cfg_path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location("cfg_two_frames_ep24", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "roi_srides")
    assert isinstance(module.roi_srides, list)
    assert module.roi_srides == [16]