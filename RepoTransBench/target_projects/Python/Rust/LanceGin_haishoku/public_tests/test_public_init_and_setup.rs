use std::path::Path;

#[test]
fn test_init_module_exists() {
    let path = Path::new("src/lib.rs"); // src/lib.rs replaces haishoku/__init__.py
    assert!(path.exists());
}

#[test]
fn test_alg_module_exists() {
    let path = Path::new("src/alg.rs");
    assert!(path.exists());
}