// Translation of uuslug/tests/test_init.py to Rust

#[test]
fn test_import_all() {
    // In Rust, symbols are statically imported, but we test they exist
    assert!(crate::uuslug::slugify as fn(&str) -> String != std::ptr::null_mut());
    assert!(crate::uuslug::uuslug as fn(&str, &dyn std::any::Any) -> String != std::ptr::null_mut());
}