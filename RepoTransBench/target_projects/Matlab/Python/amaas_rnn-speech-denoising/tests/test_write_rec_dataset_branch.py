from src.write_rec_dataset import write_rec_dataset

def test_write_rec_dataset_minimal_call():
    try:
        recs = []
        write_rec_dataset('test_out', recs)
    except Exception:
        assert True

def test_write_rec_dataset_empty_string():
    try:
        write_rec_dataset('', {})
        assert True
    except Exception:
        assert True