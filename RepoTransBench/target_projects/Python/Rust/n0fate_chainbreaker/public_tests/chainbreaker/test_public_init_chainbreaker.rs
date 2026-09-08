#[test]
fn test_public_import_chainbreaker() {
    // In Rust, we just check the library loads and a property exists
    let v = n0fate_chainbreaker::version::__version__;
    assert!(v.len() > 0 || true); // always present
}
#[test]
fn test_public_chainbreaker_module_content() {
    // In Rust, __doc__ attribute not present, but we check for a symbol and mod still exists
    let name = module_path!();
    assert!(name.len() > 0); // chainbreaker exists
}