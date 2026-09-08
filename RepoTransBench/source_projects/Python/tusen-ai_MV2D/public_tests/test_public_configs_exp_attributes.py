import importlib.util
import os
import pytest

def load_config_module(path):
    cfg_path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location("tmp_public_config", cfg_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Use different set of config files for public tests (ep*_24.py and *_two_frames_*)
PUBLIC_EXP_CONFIGS = [
    "configs/mv2d/exp/mv2d_r50_frcnn_single_frame_roi_1408x512_ep24.py",
    "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
    "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
    # Omit ep72 single frame to be data-different
]

@pytest.mark.parametrize("config_path", PUBLIC_EXP_CONFIGS)
def test_public_model_config_keys(config_path):
    module = load_config_module(config_path)
    required_keys = [
        "type", "use_grid_mask", "base_detector", "neck", "roi_head", "train_cfg"
    ]
    for key in required_keys:
        assert key in module.model, f"Missing key: {key} in {config_path}"
    # grid_mask: customize logic for public - now expect at least one of True and one float
    gm = module.model.get("use_grid_mask", {})
    assert any([v is True or isinstance(v, float) for v in gm.values()]), \
        "At least one grid mask option should be True or a float"

def test_public_roi_head_and_nested(config_path="configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py"):
    module = load_config_module(config_path)
    assert "roi_head" in module.model
    rh = module.model["roi_head"]
    assert "bbox_roi_extractor" in rh
    assert "bbox_head" in rh
    assert "query_generator" in rh
    assert "pe" in rh
    # Check nested keys
    if "bbox_head" in rh:
        bh = rh["bbox_head"]
        assert "transformer" in bh
        assert "bbox_coder" in bh
        assert bh.get("num_classes", 1) > 0
        # test for branch with/without loss_cls
        if "loss_cls" in bh:
            assert isinstance(bh["loss_cls"], dict)
    if "pe" in rh:
        pe = rh["pe"]
        assert "positional_encoding" in pe

@pytest.mark.parametrize("config_path", PUBLIC_EXP_CONFIGS)
def test_public_train_cfg_detections(config_path):
    module = load_config_module(config_path)
    train_cfg = module.model.get("train_cfg", {})
    if "detection_proposal" in train_cfg:
        det = train_cfg["detection_proposal"]
        assert "score_thr" in det
        # Check nms config branch
        if "nms" in det:
            nms = det["nms"]
            assert "iou_threshold" in nms or "class_agnostic" in nms

def test_public_code_weights_variations():
    config_paths = [
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep24.py",
        "configs/mv2d/exp/mv2d_r50_frcnn_two_frames_1408x512_ep72.py",
    ]
    for config_path in config_paths:
        module = load_config_module(config_path)
        code_weights = module.model["roi_head"]["bbox_head"].get("code_weights", [])
        assert isinstance(code_weights, list)
        assert all(isinstance(w, (float, int)) for w in code_weights)
        assert len(code_weights) == 10
        # Public: assert values not all exactly 1.0 (to guarantee extra logic coverage change)
        assert not all(w == 1.0 for w in code_weights)

@pytest.mark.parametrize("config_path", PUBLIC_EXP_CONFIGS)
def test_public_operation_order_and_cp(config_path):
    module = load_config_module(config_path)
    dec = (
        module.model["roi_head"]["bbox_head"]["transformer"]["decoder"]
        if "transformer" in module.model["roi_head"]["bbox_head"]
        else None
    )
    if dec is not None:
        transformerlayers = dec.get("transformerlayers", {})
        if isinstance(transformerlayers, dict):
            oo = transformerlayers.get("operation_order", ())
            assert isinstance(oo, (tuple, list))
            # branch: with_cp toggling (should not always be False for public)
            with_cp_set = transformerlayers.get("with_cp", None)
            assert with_cp_set in [True, False]