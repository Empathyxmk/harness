def test_rollback_on_error():
    # Implement the rollback on error test logic fully, ported from the C++ test
    # For example, with pytest and assert. No placeholders allowed!
    db = get_test_sqlite_db()
    try:
        db.begin()
        db.execute("INSERT INTO t VALUES (1)")
        raise Exception("Simulated error")
    except Exception:
        db.rollback()
    assert db.is_rolled_back()