import importlib.util
import os

def test_public_configs_data_two_frames_executable():
    # Use two_frames.py (different from single_frame.py in existing tests) for public test
    path = "configs/mv2d/data/two_frames.py"
    cfg_path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location("cfg_two_frames", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Ensure core things are present
    assert hasattr(module, "class_names")
    assert len(module.class_names) > 0
    assert hasattr(module, "train_pipeline")
    assert isinstance(module.train_pipeline, list)
    assert hasattr(module, "test_pipeline")
    assert hasattr(module, "data")
    assert isinstance(module.data, dict)
    assert hasattr(module, "point_cloud_range")
    assert hasattr(module, "input_modality")
    # Check for expected keys
    assert "train" in module.data
    assert "val" in module.data
    assert "test" in module.data or "val" in module.data  # Accept test or val as usable data

def test_public_configs_data_two_frames_edge_cases():
    # Ensure all pipeline stages have 'type' key and it's a non-empty string
    path = "configs/mv2d/data/two_frames.py"
    cfg_path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location("cfg_edge_two", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for idx, stage in enumerate(module.train_pipeline):
        assert isinstance(stage, dict)
        assert "type" in stage
        assert isinstance(stage["type"], str)
        assert len(stage["type"]) > 0