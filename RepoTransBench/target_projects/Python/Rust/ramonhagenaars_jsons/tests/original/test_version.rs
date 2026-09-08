#[test]
fn test_version() {
    // Simulate Rust crate version "major.minor.patch"
    let crate_version = env!("CARGO_PKG_VERSION");
    assert_eq!(3, crate_version.split('.').count());
}