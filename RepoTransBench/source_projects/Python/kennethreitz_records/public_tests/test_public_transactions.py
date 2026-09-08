import pytest
import records

def test_transactions_commit_public(db):
    db.query("CREATE TABLE books (isbn varchar(13), title text)")
    with db.transaction():
        db.query("INSERT INTO books (isbn, title) VALUES (:isbn, :title)", isbn="1234567890123", title="Great Book")
    res = db.query("SELECT * FROM books WHERE isbn = :isbn", isbn="1234567890123")
    assert res.first()['title'] == "Great Book"

def test_transactions_rollback_public(db):
    db.query("CREATE TABLE t1 (foo text)")
    try:
        with db.transaction():
            db.query("INSERT INTO t1 (foo) VALUES (:foo)", foo="tempvalue")
            raise ValueError("trigger rollback")
    except ValueError:
        pass
    out = db.query("SELECT * FROM t1")
    assert out.first() is None

def test_transactions_nested_public(db):
    db.query("CREATE TABLE t2 (id integer)")
    with db.transaction():
        db.query("INSERT INTO t2 (id) VALUES (:id)", id=1)
        with db.transaction():
            db.query("INSERT INTO t2 (id) VALUES (:id)", id=2)
    out = list(db.query("SELECT * FROM t2"))
    assert {x['id'] for x in out} == {1, 2}

def test_transactions_multi_statement_commit_public(db):
    db.query("CREATE TABLE accounts (id integer, balance integer)")
    with db.transaction():
        db.query("INSERT INTO accounts (id, balance) VALUES (1, 200)")
        db.query("UPDATE accounts SET balance = balance + 150")
    out = db.query("SELECT balance FROM accounts WHERE id = 1")
    assert out.first()['balance'] == 350

def test_transactions_context_manager_return_public(db):
    db.query("CREATE TABLE chess (piece text)")
    with db.transaction() as trans:
        assert trans
        db.query("INSERT INTO chess (piece) VALUES (:piece)", piece='rook')
    data = db.query("SELECT piece FROM chess")
    assert data.first()['piece'] == 'rook'

def test_transactions_rollback_exception_instance_public(db):
    db.query("CREATE TABLE mus (sound text)")
    class RollEx(Exception): pass

    try:
        with db.transaction():
            db.query("INSERT INTO mus (sound) VALUES (:sound)", sound="chirp")
            raise RollEx()
    except RollEx:
        pass
    data = db.query("SELECT * FROM mus")
    assert data.first() is None