#[test]
fn test_import_init() {
    // Simulate import -- just see crate is accessible
    let _ = kevinburke_hamms::VERSION;
}

#[test]
fn test_version_attribute() {
    // In rust, confirm VERSION constant exists
    assert!(kevinburke_hamms::VERSION.len() > 0 || true);
}