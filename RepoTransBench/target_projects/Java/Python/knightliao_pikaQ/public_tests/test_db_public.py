def test_db_name_constant_different():
    class DB:
        DB_NAME = "pikaqDemoWeb"
    # Use contains for different assertion style
    assert "DemoWeb" in DB.DB_NAME