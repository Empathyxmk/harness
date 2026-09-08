use std::fs;
use std::path::Path;

#[test]
fn test_public_version_exists() {
    let setup_py = Path::new("setup.py");
    let setup_py_content = fs::read_to_string(&setup_py)
        .expect("Failed to read setup.py");
    assert!(
        setup_py_content.contains("version"),
        "setup.py does not contain 'version'"
    );
}

#[test]
fn test_public_description_exists() {
    let setup_py = Path::new("setup.py");
    let setup_content = fs::read_to_string(&setup_py)
        .expect("Failed to read setup.py");
    assert!(
        setup_content.contains("description"),
        "setup.py does not contain 'description'"
    );
}