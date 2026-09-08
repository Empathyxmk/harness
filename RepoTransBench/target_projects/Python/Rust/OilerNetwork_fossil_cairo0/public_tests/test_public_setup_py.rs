use std::fs;
use std::io::Read;
use std::path::Path;

#[test]
fn test_public_setup_py_exists() {
    // Test that setup.py file exists - public variant.
    // Use is_file instead of exists.
    assert!(
        Path::new("setup.py").is_file(),
        "setup.py file does not exist or is not a file"
    );
}

#[test]
fn test_public_imports() {
    // Test that setup.py can be imported/syntax-checked (excluding SCM/build logic)
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
fn test_public_metadata() {
    // Test that setup.py includes different expected metadata fields (public variant)
    let mut file = fs::File::open("setup.py").expect("unable to open setup.py");
    let mut content = String::new();
    file.read_to_string(&mut content).expect("unable to read setup.py");
    // Use a different field from the project metadata, such as install_requires and setuptools
    assert!(
        content.contains("install_requires"),
        "setup.py missing 'install_requires' field"
    );
    assert!(
        content.contains("setuptools"),
        "setup.py missing 'setuptools' field"
    );
}