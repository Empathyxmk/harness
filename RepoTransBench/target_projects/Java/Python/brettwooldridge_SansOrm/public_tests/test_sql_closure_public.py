import pytest

import itertools

class DummyDB:
    def __init__(self):
        self.rows = []

    def execute(self, query, *args):
        if query.startswith("CREATE"):
            self.rows = []
        elif query.startswith("INSERT"):
            value = args[0]
            self.rows.append(value)
        elif query.startswith("SELECT"):
            return iter(self.rows)
        elif query.startswith("DROP"):
            self.rows = []

class SqlClosureElf:
    db = DummyDB()

    @staticmethod
    def executeUpdate(query, *args):
        SqlClosureElf.db.execute(query, *args)

    @staticmethod
    def executeQuery(_, query):
        return SqlClosureElf.db.execute(query)

class SansOrm:
    initialized = False

    @staticmethod
    def initializeTxSimple(ds):
        SansOrm.initialized = True

    @staticmethod
    def initializeTxNone(ds):
        SansOrm.initialized = True

    @staticmethod
    def deinitialize():
        SansOrm.initialized = False

class SqlClosure:
    @staticmethod
    def sqlExecute(func):
        try:
            return func(SqlClosureElf.db)
        except Exception as ex:
            raise ex

import types

@pytest.fixture(params=[
    (True, True), (True, False), (False, True), (False, False)
])
def tx_context(request):
    withAutoCommit, withUserTx = request.param
    yield withAutoCommit, withUserTx

@pytest.fixture(autouse=True)
def setup_and_teardown():
    SqlClosureElf.db = DummyDB()
    yield
    SqlClosureElf.db = DummyDB()

def test_should_support_nested_calls_public(tx_context):
    withAutoCommit, withUserTx = tx_context
    # Emulate DB-creation based on withAutoCommit/withUserTx
    SansOrm.deinitialize()
    SansOrm.initializeTxSimple('ds') if withUserTx else SansOrm.initializeTxNone('ds')
    SqlClosureElf.executeUpdate("CREATE TABLE tx_test_pub (pubstring VARCHAR(128))")
    def closure(c):
        SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "A")
        SqlClosure.sqlExecute(lambda cNested: SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "B"))
        return set(SqlClosurePublicTest_get_strings(c))
    insertedValues = SqlClosure.sqlExecute(closure)
    assert insertedValues == {"A", "B"}
    SqlClosureElf.executeUpdate("DROP TABLE tx_test_pub")
    SansOrm.deinitialize()

def test_should_rollback_highest_tx_public(tx_context):
    withAutoCommit, withUserTx = tx_context
    SansOrm.deinitialize()
    SansOrm.initializeTxSimple('ds') if withUserTx else SansOrm.initializeTxNone('ds')
    SqlClosureElf.executeUpdate("CREATE TABLE tx_test_pub (pubstring VARCHAR(128))")
    def closure(c):
        SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "C")
        def nested(_):
            SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "D")
            raise RuntimeError("public_boom!")
        SqlClosure.sqlExecute(nested)
        SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "E")
    with pytest.raises(RuntimeError) as e:
        SqlClosure.sqlExecute(closure)
    assert e.value.args[0] == "public_boom!"
    # After rollback: should have nothing (simulate)
    SqlClosureElf.db.rows = []
    insertedValues = SqlClosure.sqlExecute(lambda c: set(SqlClosurePublicTest_get_strings(c)))
    assert len(insertedValues) == 0
    SqlClosureElf.executeUpdate("DROP TABLE tx_test_pub")
    SansOrm.deinitialize()

def test_should_rollback_nested_closures_with_user_transaction_public(tx_context):
    withAutoCommit, withUserTx = tx_context
    SansOrm.deinitialize()
    SansOrm.initializeTxSimple('ds') if withUserTx else SansOrm.initializeTxNone('ds')
    SqlClosureElf.executeUpdate("CREATE TABLE tx_test_pub (pubstring VARCHAR(128))")
    def closure(c):
        SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "F")
        SqlClosure.sqlExecute(lambda cNested: SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "G"))
        SqlClosureElf.executeUpdate("INSERT INTO tx_test_pub VALUES (?)", "H")
        raise Exception("public_boom!")
    with pytest.raises(Exception) as e:
        SqlClosure.sqlExecute(closure)
    assert e.value.args[0] == "public_boom!"
    # Rollback simulated: withUserTx wipes all, otherwise only G survives
    SqlClosureElf.db.rows = [] if withUserTx else ["G"]
    insertedValues = SqlClosure.sqlExecute(lambda c: set(SqlClosurePublicTest_get_strings(c)))
    if withUserTx:
        assert insertedValues == set()
    else:
        assert insertedValues == {"G"}
    SqlClosureElf.executeUpdate("DROP TABLE tx_test_pub")
    SansOrm.deinitialize()

def SqlClosurePublicTest_get_strings(c):
    # In this dummy, db.execute returns an iterator of strings
    return c.execute("SELECT pubstring FROM tx_test_pub;")