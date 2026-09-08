use std::fs;
use std::path::Path;

#[test]
fn test_setup_py_exists_and_has_setup_call() {
    let path = Path::new("setup.py");
    assert!(
        path.exists(),
        "setup.py file does not exist in project root"
    );
    let content = fs::read_to_string(&path)
        .expect("Failed to read setup.py");
    assert!(
        content.contains("setup("),
        "setup.py does not contain 'setup('"
    );
    assert!(
        content.contains("__name__"),
        "setup.py does not contain '__name__'"
    );
}