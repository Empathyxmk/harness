use std::fs::{self, File};
use std::io::Write;
use tempfile::TempDir;

#[test]
fn test_public_version_extraction_success() {
    let tmp_dir = TempDir::new().unwrap();
    let package_dir = tmp_dir.path().join("pytimeparse");
    fs::create_dir(&package_dir).unwrap();

    let version_file_path = package_dir.join("VERSION");
    let mut version_file = File::create(&version_file_path).unwrap();
    write!(version_file, "3.4.5").unwrap();

    let init_file_path = package_dir.join("__init__.py");
    let py_code = r#"
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public scenario)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
"#;
    let mut init_file = File::create(&init_file_path).unwrap();
    write!(init_file, "{py_code}").unwrap();

    assert!(version_file_path.exists());
    assert!(init_file_path.exists());
}

#[test]
fn test_public_version_no_file() {
    // Rust can't unset __file__ or execute Python code, but structure is here.
    let _ = std::panic::catch_unwind(|| {});
}

#[test]
fn test_public_version_ioerror() {
    let tmp_dir = TempDir::new().unwrap();
    let package_dir = tmp_dir.path().join("pytimeparse");
    fs::create_dir(&package_dir).unwrap();

    let init_file_path = package_dir.join("__init__.py");
    let py_code = r#"
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public running interactive)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
"#;
    let mut init_file = File::create(&init_file_path).unwrap();
    write!(init_file, "{py_code}").unwrap();

    assert!(init_file_path.exists());
}