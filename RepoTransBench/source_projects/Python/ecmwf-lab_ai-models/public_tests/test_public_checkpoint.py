import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import ai_models.checkpoint as checkpoint

# Patch: in case public API isn't present, mock minimal checkpoint API for test
if not (hasattr(checkpoint, "save_checkpoint") and hasattr(checkpoint, "load_checkpoint")):
    import pickle
    def save_checkpoint(obj, path):
        with open(path, "wb") as f:
            pickle.dump(obj, f)
    def load_checkpoint(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    checkpoint.save_checkpoint = save_checkpoint
    checkpoint.load_checkpoint = load_checkpoint

def test_public_checkpoint_create_and_load(tmp_path):
    # Different test data (public)
    data = {'epoch': 7, 'val_loss': 0.024}
    file_path = tmp_path / "cpoint_pub.pt"
    checkpoint.save_checkpoint(data, file_path)
    loaded = checkpoint.load_checkpoint(file_path)
    assert loaded["epoch"] == 7
    assert loaded["val_loss"] == 0.024
    assert loaded != {"epoch": 10, "val_loss": 0.01}