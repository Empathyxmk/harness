import pytest

class TableFactory:
    pass

class NexmarkTableSourceFactory(TableFactory):
    def __str__(self):
        return f"NexmarkTableSourceFactory({id(self)})"

def test_factory_class_type():
    factory = NexmarkTableSourceFactory()
    assert isinstance(factory, NexmarkTableSourceFactory)

def test_factory_to_string_not_null():
    factory = NexmarkTableSourceFactory()
    assert factory.__str__() is not None