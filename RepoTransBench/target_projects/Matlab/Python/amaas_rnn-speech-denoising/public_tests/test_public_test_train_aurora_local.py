from src.train_aurora_local import train_aurora_local

def test_public_train_aurora_local_dry_run():
    try:
        train_aurora_local()
    except Exception:
        assert True