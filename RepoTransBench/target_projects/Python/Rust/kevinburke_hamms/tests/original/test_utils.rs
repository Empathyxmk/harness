#[test]
fn test_utils_dummy() {
    // Always true
    assert!(true);
}

#[test]
fn test_import_get_header() {
    // Test that get_header function exists and returns a string
    let val = kevinburke_hamms::get_header();
    assert_eq!(val, "dummy-header");
}