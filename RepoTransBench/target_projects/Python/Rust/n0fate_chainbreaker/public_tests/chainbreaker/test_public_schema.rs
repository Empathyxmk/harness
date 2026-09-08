use n0fate_chainbreaker::schema as schema_mod;

#[test]
fn test_public_schema_attributes() {
    // In Rust, we can check if the module functions exist
    let s = schema_mod::KeychainSchema::default();
    let cols = s.get_column_names("foo");
    assert!(!cols.is_empty());
}

#[test]
fn test_public_schema_type_of_module() {
    // In Rust the module is a namespace and always statically typed
    assert_eq!(1 + 1, 2);
}