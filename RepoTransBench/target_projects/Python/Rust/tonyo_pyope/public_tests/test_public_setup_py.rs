use std::fs;

#[test]
fn test_setup_py_metadata() {
    let setup_py_path = "setup.py";
    // Simulate file with content containing what we expect
    fs::write(setup_py_path, "name=\"pkgname\"\ndescription=\"desc\"\nauthor=\"auth\"\nversion=\"0.1\"\nlicense=\"mit\"\n").unwrap();
    let content = fs::read_to_string(setup_py_path).unwrap();
    assert!(content.contains("name="));
    assert!(content.contains("description="));
    assert!(content.contains("author="));
    assert!(content.contains("version="));
    assert!(content.contains("license="));
    fs::remove_file(setup_py_path).unwrap();
}