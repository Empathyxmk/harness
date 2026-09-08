import pytest
from protofuzz import pbimport

def test_import_proto_module_smoke():
    # The canonical test proto
    result = pbimport.import_proto_module("protofuzz/tests/test.proto")
    assert hasattr(result, "DESCRIPTOR")

def test_resolve_include_path_exists(tmp_path):
    test_proto = tmp_path / "abc.proto"
    test_proto.write_text("syntax = 'proto3';")
    # Should resolve the same path if it exists
    assert pbimport.resolve_include_path(str(test_proto), [str(tmp_path)]) == str(test_proto)

def test_resolve_include_path_not_found(tmp_path):
    assert pbimport.resolve_include_path("idontexist.proto", [str(tmp_path)]) is None

def test_parse_proto_imports_simple():
    text = 'import "foo.proto";\n'
    result = pbimport.parse_proto_imports(text)
    assert "foo.proto" in result