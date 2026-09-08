from src.write_rec_dataset import write_rec_dataset

def test_write_rec_dataset_missing_directory():
    try:
        write_rec_dataset('definitely_non_existing_path', 'dummy.mlf', [])
        assert True
    except Exception:
        assert False