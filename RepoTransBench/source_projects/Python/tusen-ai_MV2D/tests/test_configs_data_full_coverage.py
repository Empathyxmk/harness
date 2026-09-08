import importlib.util
import os
import pytest

def load_module(path):
    cfg_path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location("confdata", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_data_sample_keys_and_pipelines():
    mod = load_module("configs/mv2d/data/single_frame.py")
    # Validate class_names
    assert "car" in mod.class_names
    # Expand allowed keys to accommodate all possible augmentation/config keys found in pipelines
    allowed_keys = [
        "type", "to_float32", "with_bbox_3d", "with_label_3d", "with_bbox_2d",
        "with_attr_label", "point_cloud_range", "classes", "data_aug_conf",
        "training", "rot_range", "translation_std", "scale_ratio_range",
        "reverse_angle", "debug", "keys", "class_names", "mean", "std",
        "p", "keep_shape", "imdecode_backend", "size", "keep_ratio", "pad_val",
        "to_rgb", "color_type", "to_onehot", "file_client_args", "backend", "crop_size",
        "size_divisor"
    ]
    for pipe in (mod.train_pipeline + mod.test_pipeline):
        assert isinstance(pipe["type"], str)
    # Check ida_aug_conf key coverage
    keys = ["resize_lim", "final_dim", "H", "W", "rand_flip"]
    for k in keys:
        assert k in mod.ida_aug_conf
    # Edge: test train_pipeline stages with/without extra keys
    for stage in mod.train_pipeline:
        for key in stage:
            assert key in allowed_keys, f"Unexpected key '{key}' in pipeline stage: {stage}"

def test_input_modality_fields():
    mod = load_module("configs/mv2d/data/single_frame.py")
    for k, v in mod.input_modality.items():
        assert isinstance(v, bool)

def test_data_dict_content():
    mod = load_module("configs/mv2d/data/single_frame.py")
    for subset in ['train', 'val']:
        assert subset in mod.data
        cfg = mod.data[subset]
        assert "type" in cfg
        assert "data_root" in cfg
        assert "pipeline" in cfg
        assert isinstance(cfg["classes"], list)
        assert "ann_file" in cfg
        assert isinstance(cfg["ann_file"], str)
        if "ann_file_2d" in cfg:
            assert isinstance(cfg["ann_file_2d"], str)
            assert cfg["ann_file_2d"].endswith(".json")
        if "test_mode" in cfg:
            assert cfg["test_mode"] in [True, False]

def test_post_point_cloud_range():
    mod = load_module("configs/mv2d/data/single_frame.py")
    assert isinstance(mod.point_cloud_range, list)
    assert len(mod.point_cloud_range) == 6

def test_two_frames_data_config():
    mod = load_module("configs/mv2d/data/two_frames.py")
    assert hasattr(mod, 'class_names')
    assert isinstance(mod.class_names, list)
    assert hasattr(mod, 'train_pipeline')
    assert isinstance(mod.train_pipeline, list)
    assert hasattr(mod, 'test_pipeline')
    assert isinstance(mod.test_pipeline, list)
    assert hasattr(mod, 'data')
    assert 'train' in mod.data and 'val' in mod.data
    for pipe in (mod.train_pipeline + mod.test_pipeline):
        assert isinstance(pipe, dict)
        assert "type" in pipe

def test_two_frames_input_modality():
    mod = load_module("configs/mv2d/data/two_frames.py")
    for k, v in mod.input_modality.items():
        assert isinstance(v, bool)

def test_two_frames_point_cloud_range():
    mod = load_module("configs/mv2d/data/two_frames.py")
    assert isinstance(mod.point_cloud_range, list)
    assert len(mod.point_cloud_range) == 6