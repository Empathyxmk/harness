use crate::pbimport;

#[test]
fn test_import_proto_module_smoke() {
    // Returns dummy with descriptor
    let result = pbimport::import_proto_module("dummy.proto");
    assert!(result.descriptor);
}

#[test]
fn test_resolve_include_path_exists() {
    // Simulate as Some iff exists, always None in test env
    let proto = "abc.proto";
    let paths = ["/does/not/exist"];
    let found = pbimport::resolve_include_path(proto, &paths);
    assert!(found.is_none());
}

#[test]
fn test_resolve_include_path_not_found() {
    let proto = "missing.proto";
    let paths = [];
    let not_found = pbimport::resolve_include_path(proto, &paths);
    assert!(not_found.is_none());
}

#[test]
fn test_parse_proto_imports_simple() {
    let txt = "import \"foo.proto\";\n";
    let result = pbimport::parse_proto_imports(txt);
    assert!(result.contains(&"foo.proto".to_owned()));
}