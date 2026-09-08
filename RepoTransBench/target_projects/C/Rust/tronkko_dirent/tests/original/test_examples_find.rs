/// Rust translation of tests/test_examples_find.c

use tempfile::tempdir;
use std::fs::{self, File};
use tronkko_dirent_rust::examples::find::_main;

#[test]
fn test_find_default_lists_dot() {
    let args = ["find"];
    let result = _main(&args);
    assert_eq!(result, 0, "find with no args should succeed on .");
}

#[test]
fn test_find_valid_dir() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("file.txt");
    File::create(&file_path).unwrap();
    let args = ["find", dir.path().to_str().unwrap()];
    let result = _main(&args);
    assert_eq!(result, 0, "find on valid dir should succeed");
}

#[test]
fn test_find_invalid_dir() {
    let args = ["find", "DOESNOTEXISTFIND"];
    let result = _main(&args);
    assert_eq!(result, 1, "find on invalid dir should fail");
}