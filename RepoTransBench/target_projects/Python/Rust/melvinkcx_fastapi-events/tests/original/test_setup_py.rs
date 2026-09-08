use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::TempDir;

#[test]
fn test_get_version_and_long_desc() {
    // Setup temp directory
    let tmp_dir = TempDir::new().expect("create temp dir");
    let tmp_path = tmp_dir.path();

    let mut fapi_dir = PathBuf::from(tmp_path);
    fapi_dir.push("fastapi_events");
    fs::create_dir(&fapi_dir).expect("create fastapi_events dir");

    let mut initfile = fapi_dir.clone();
    initfile.push("__init__.py");
    let mut initf = File::create(&initfile).expect("create __init__.py");
    initf.write_all(b"__version__ = \"9.0.1\"\n").expect("write to __init__.py");

    let mut readmefile = PathBuf::from(tmp_path);
    readmefile.push("README.md");
    let mut readf = File::create(&readmefile).expect("create README.md");
    readf.write_all(b"Hello this is a desc!").expect("write to README.md");

    // Simulate a minimal `setup.py` logic in Rust
    let get_version = || {
        let content = std::fs::read_to_string(&initfile).unwrap();
        for line in content.lines() {
            if line.trim().starts_with("__version__ =") {
                let version = line
                    .split('=')
                    .nth(1)
                    .unwrap()
                    .trim()
                    .trim_matches('"');
                return version.to_string();
            }
        }
        "".to_string()
    };

    let get_long_description = || {
        std::fs::read_to_string(&readmefile).unwrap()
    };

    assert_eq!(get_version(), "9.0.1");
    let long_desc = get_long_description();
    assert!(long_desc.contains("desc"));
}