use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::TempDir;

fn create_fake_init_py(path: &PathBuf, version_str: &str) {
    let mut fapi_path = path.clone();
    fapi_path.push("fastapi_events");
    fs::create_dir_all(&fapi_path).expect("create dir");
    let mut file = File::create(fapi_path.join("__init__.py")).expect("create __init__.py");
    writeln!(file, "__version__ = '{}'", version_str).expect("write version");
}

fn create_fake_readme(path: &PathBuf, content: &str) {
    let mut path = path.clone();
    let mut file = File::create(path.join("README.md")).expect("create README.md");
    writeln!(file, "{}", content).expect("write README");
}

fn create_fake_setup_py(path: &PathBuf) {
    let mut path = path.clone();
    let mut file = File::create(path.join("setup.py")).expect("create setup.py");
    writeln!(
        file,
        "import os
def get_version():
    package_init = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fastapi_events', '__init__.py')
    with open(package_init) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('\"\\'')
def get_long_description():
    with open('README.md', 'r') as fh:
        return fh.read()"
    )
    .expect("write setup.py");
}

#[test]
fn test_get_version_and_long_desc_public() {
    let tmp_dir = TempDir::new().expect("create temp dir");
    let tmp_path = PathBuf::from(tmp_dir.path());

    create_fake_init_py(&tmp_path, "7.5.1-pub");
    let public_readme = "## My Awesome Public Package

A library for cool public event handling.

Public Test Coverage Section
See more at: https://public.example.com
";
    create_fake_readme(&tmp_path, public_readme);
    create_fake_setup_py(&tmp_path);

    // Simulate the get_version and get_long_description as in test_setup_py
    let initfile = tmp_path.join("fastapi_events").join("__init__.py");
    let get_version = || {
        let content = std::fs::read_to_string(&initfile).unwrap();
        for line in content.lines() {
            if line.trim().starts_with("__version__ =") {
                let version = line
                    .split('=')
                    .nth(1)
                    .unwrap()
                    .trim()
                    .trim_matches('\'');
                return version.to_string();
            }
        }
        "".to_string()
    };

    let readmefile = tmp_path.join("README.md");
    let get_long_description = || std::fs::read_to_string(&readmefile).unwrap();

    let version = get_version();
    assert_eq!(version, "7.5.1-pub");
    let long_desc = get_long_description();
    assert!(long_desc.contains("Public Test Coverage Section"));
    assert!(long_desc.starts_with("## My Awesome Public Package"));
    assert!(long_desc.contains("https://public.example.com"));
}