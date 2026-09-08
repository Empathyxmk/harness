import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../local-llm")))
import modelfiles

def test_public_model_from_path_shortformat():
    # Use a different path from private test
    assert modelfiles.model_from_path("/mnt/bob/models/elephant/banana.Q4_1.gguf") == ("elephant", "banana.Q4_1.gguf")

def test_public_model_from_path_longer():
    # Unusual path structure
    assert modelfiles.model_from_path("/home/user/some/other/hippo/hippopotamus.Q5_0.gguf") == ("hippo", "hippopotamus.Q5_0.gguf")