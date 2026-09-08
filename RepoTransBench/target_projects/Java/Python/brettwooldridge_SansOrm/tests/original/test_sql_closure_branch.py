import pytest

class DataSourceStub:
    pass

class SqlClosure:
    _default_data_source = None

    @classmethod
    def setDefaultDataSource(cls, ds):
        cls._default_data_source = ds

    def __init__(self, *args):
        if not args and SqlClosure._default_data_source is None:
            raise RuntimeError("No DataSource provided")

@pytest.fixture(autouse=True)
def cleanup():
    yield
    SqlClosure.setDefaultDataSource(None)

def test_default_constructor_throws_if_no_data_source():
    SqlClosure.setDefaultDataSource(None)
    with pytest.raises(RuntimeError):
        SqlClosure()

def test_other_constructors_without_default_data_source():
    ds = DataSourceStub()
    c1 = SqlClosure(ds)
    assert c1 is not None

    c2 = SqlClosure(ds, "arg1", 42)
    assert c2 is not None

    c3 = SqlClosure(SqlClosure(ds))
    assert c3 is not None

    c4 = SqlClosure("a", "b")
    assert c4 is not None

def test_set_default_data_source():
    ds = DataSourceStub()
    SqlClosure.setDefaultDataSource(ds)
    c = SqlClosure()
    assert c is not None