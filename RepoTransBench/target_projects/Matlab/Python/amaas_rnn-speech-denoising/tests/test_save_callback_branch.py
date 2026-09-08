import pytest
from src.save_callback import save_callback

def test_save_callback_empty_args():
    with pytest.raises(TypeError):
        save_callback()

def test_save_callback_filename_only():
    with pytest.raises(TypeError):
        save_callback('dummy.mat')