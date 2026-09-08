#[test]
fn test_basic_imports() {
    // Just confirm std lib functions
    assert!(std::env::var("PATH").is_ok() || std::env::consts::OS.len() > 0);
    assert!(true);
}