def test_db_name_constant():
    class DB:
        DB_NAME = "pikaqDemoWeb"
    assert DB.DB_NAME == "pikaqDemoWeb"