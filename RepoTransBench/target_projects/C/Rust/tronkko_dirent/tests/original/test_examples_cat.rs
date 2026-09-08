/// Rust translation of tests/test_examples_cat.c
use std::fs::{remove_file, File};
use std::io::Write;
use std::process::Command;

use tempfile::tempdir;

use tronkko_dirent_rust::examples::cat::_main;

#[test]
fn test_cat_usage_no_args() {
    // Should print usage, exit 0
    let args = ["cat"];
    let code = _main(&args);
    assert_eq!(code, 0, "cat without args should return 0");
}

#[test]
fn test_cat_valid_file() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("cat_temp.txt");
    {
        let mut f = File::create(&path).unwrap();
        write!(f, "xycatabc\n").unwrap();
    }
    let args = ["cat", path.to_str().unwrap()];
    let code = _main(&args);
    assert_eq!(code, 0, "cat on valid file should succeed");
}

#[test]
fn test_cat_file_not_exist() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("DOES_NOT_EXIST_CAT_FILE");
    let args = ["cat", path.to_str().unwrap()];
    let code = _main(&args);
    assert_eq!(code, 1, "cat on non-existent file should return error");
}