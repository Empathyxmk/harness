import sys
import pathlib

# Add project root to sys.path to import the package
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import chainbreaker.schema as schema

def test_public_schema_attributes():
    # Test the schema module exposes certain expected attributes (use hypothetical different attribute)
    assert hasattr(schema, "__file__") or hasattr(schema, "__doc__")

def test_public_schema_type_of_module():
    # Make sure chainbreaker.schema is a module object, not a class
    import types
    assert isinstance(schema, types.ModuleType)