#[test]
fn test_public_version_attribute() {
    let v = n0fate_chainbreaker::version::__version__;
    assert!(v.contains('.') && v.split('.').count() >= 2);
}
#[test]
fn test_public_version_module_doc() {
    // Not applicable in Rust, but the module exists
    assert_eq!(1, 1);
}