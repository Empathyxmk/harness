import sqlite3

def test_public_sqlite_in_memory_insert():
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("CREATE TABLE test_public(id int, name text)")
    cur.execute("INSERT INTO test_public(id, name) VALUES (?, ?)", (2, "sqltest"))
    db.commit()
    cur.execute("SELECT id, name FROM test_public")
    row = cur.fetchone()
    assert row == (2, "sqltest")
    db.close()

def test_public_sqlite_unique_constraint():
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("CREATE TABLE uniq(id INTEGER PRIMARY KEY, val INTEGER UNIQUE)")
    cur.execute("INSERT INTO uniq(val) VALUES (44)")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO uniq(val) VALUES (44)")
    db.close()