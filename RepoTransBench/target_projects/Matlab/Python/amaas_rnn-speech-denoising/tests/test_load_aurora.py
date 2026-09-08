from src.load_aurora import load_aurora

def test_load_aurora_nonexistent_path():
    mat, lab = load_aurora('definitely_non_existing_path', 'train')
    assert mat is None or mat == [] or not mat
    assert lab is None or lab == [] or not lab