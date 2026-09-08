import pytest

class DataSourceStub:
    pass

class TransactionManagerStub:
    pass

class UserTransactionStub:
    pass

class SansOrm:
    _initialized = False

    @classmethod
    def deinitialize(cls):
        cls._initialized = False

    @classmethod
    def initializeTxNone(cls, ds):
        cls._initialized = True
        return ds

    @classmethod
    def initializeTxSimple(cls, ds):
        cls._initialized = True
        return ds

    @classmethod
    def initializeTxCustom(cls, ds, tm, ut):
        cls._initialized = True
        return ds

@pytest.fixture(autouse=True)
def setup_and_teardown():
    SansOrm.deinitialize()
    yield
    SansOrm.deinitialize()

def test_initialize_tx_none():
    ds = DataSourceStub()
    result = SansOrm.initializeTxNone(ds)
    assert result is not None
    assert result is ds

def test_initialize_tx_simple():
    ds = DataSourceStub()
    result = SansOrm.initializeTxSimple(ds)
    assert result is not None

def test_initialize_tx_custom():
    ds = DataSourceStub()
    tm = TransactionManagerStub()
    ut = UserTransactionStub()
    result = SansOrm.initializeTxCustom(ds, tm, ut)
    assert result is ds

def test_deinitialize():
    ds = DataSourceStub()
    tm = TransactionManagerStub()
    ut = UserTransactionStub()
    SansOrm.initializeTxCustom(ds, tm, ut)
    SansOrm.deinitialize()  # Should not raise