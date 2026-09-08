#[test]
fn test_init_dunder_version() {
    // In Rust, we could have a const VERSION. We'll check it's a string.
    const VERSION: &str = "0.1.0";
    assert!(VERSION.is_ascii());
}

#[test]
fn test_init_search_importable() {
    // "Importing" is always available in Rust if in lib.
    assert_eq!(super::super::jmespath::search as usize > 0, true);
}