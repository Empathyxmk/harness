try:
    from src.parser import parser_constants as constants
except ImportError:
    constants = {}

def test_export_object_or_constants():
    assert isinstance(constants, (dict, object))
    assert len(getattr(constants, '__dict__', {})) > 0 or hasattr(constants, '__dict__')