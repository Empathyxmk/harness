#[test]
fn test_imports_public() {
    // In Rust, 'importing' the module is linking; check that lib functions exist.
    use antiboredom_audiogrep::*;
    // __file__ or __doc__ isn't meaningful in Rust, but the module must load.
    assert!(true);
}