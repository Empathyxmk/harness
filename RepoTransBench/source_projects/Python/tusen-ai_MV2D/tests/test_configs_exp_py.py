import importlib.util
import os
import pytest

EXP_CONFIGS = [
    "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.py",
    "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep72.py",
    "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
    "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
]

@pytest.mark.parametrize("config_path", EXP_CONFIGS)
def test_config_loads(config_path):
    """Test that config python files can be loaded/executed without error."""
    cfg_path = os.path.abspath(config_path)
    spec = importlib.util.spec_from_file_location("config_to_test", cfg_path)
    module = importlib.util.module_from_spec(spec)
    # Should not raise
    spec.loader.exec_module(module)

    # Check basic expected attributes
    assert hasattr(module, "model")
    assert isinstance(module.model, dict)
    assert hasattr(module, "_base_")
    assert isinstance(module._base_, (list, tuple))