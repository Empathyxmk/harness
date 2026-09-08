import os
import tempfile
import shutil

class ObfDex:
    @staticmethod
    def obf(input_path, param, arr1, arr2, param3):
        if not input_path or not os.path.exists(input_path):
            return
        if os.path.isfile(input_path):
            return
        # Directory - just don't do anything for empty
        for name in os.listdir(input_path):
            if name.endswith('.dex'):
                pass  # Fake: would process .dex files

def test_obf_non_existent_dir():
    # Should not raise, input dir does not exist
    ObfDex.obf("not/a/real/directory", 1, [], [], None)

def test_obf_single_file_that_is_not_dex():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        ObfDex.obf(tmp_path, 1, [], [], None)
    finally:
        os.remove(tmp_path)

def test_obf_empty_directory():
    dir_path = os.path.join(tempfile.gettempdir(), f"empty_dir_for_obf_test_{os.getpid()}")
    os.makedirs(dir_path, exist_ok=True)
    try:
        ObfDex.obf(dir_path, 1, [], [], None)
    finally:
        shutil.rmtree(dir_path)