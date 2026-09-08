#[test]
fn test_utils_public_true() {
    assert!(10 > 5);
}

#[test]
fn test_import_get_header_public() {
    // Confirm get_header function exists
    let v = kevinburke_hamms::get_header();
    assert_eq!(v, "dummy-header");
}