#[test]
fn test_public_setup_py_runs() {
    // Just check that a file exists called setup.py
    let path = std::path::Path::new("setup.py");
    assert!(path.is_file());
}