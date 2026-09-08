use std::fs;
use std::io::Read;
use std::path::Path;

#[test]
fn test_setup_py_exists() {
    // Test that setup.py file exists.
    assert!(Path::new("setup.py").exists(), "setup.py file does not exist");
}

#[test]
fn test_imports() {
    // Test that setup.py can be "imported" (syntax check), ignoring SCM/build errors.
    use std::process::Command;

    // Try running a syntax check (equivalent to import test). We use `python3 -m py_compile setup.py`.
    let output = Command::new("python3")
        .arg("-m")
        .arg("py_compile")
        .arg("setup.py")
        .output()
        .expect("failed to execute python3");
    let stderr = String::from_utf8_lossy(&output.stderr).to_lowercase();
    if !output.status.success() {
        // Allow version/build/scm errors but not syntax errors
        assert!(
            stderr.contains("scm") || stderr.contains("build"),
            "Import (py_compile) failed: {}",
            stderr
        );
    }
}

#[test]
fn test_metadata() {
    // Test that setup.py includes expected metadata fields.
    let mut file = fs::File::open("setup.py").expect("unable to open setup.py");
    let mut content = String::new();
    file.read_to_string(&mut content).expect("unable to read setup.py");
    assert!(
        content.contains("name"),
        "setup.py missing 'name' field"
    );
    assert!(
        content.contains("version_scheme"),
        "setup.py missing 'version_scheme' field"
    );
}