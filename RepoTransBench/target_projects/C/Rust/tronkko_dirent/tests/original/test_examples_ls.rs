/// Rust translation of tests/test_examples_ls.c

use tempfile::tempdir;
use std::fs::{self, File};
use tronkko_dirent_rust::examples::ls::_main;

#[test]
fn test_ls_default_lists_dot() {
    let args = ["ls"];
    let result = _main(&args);
    assert_eq!(result, 0, "ls with no args should succeed on .");
}

#[test]
fn test_ls_valid_dir() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("file.txt");
    File::create(&file_path).unwrap();
    let args = ["ls", dir.path().to_str().unwrap()];
    let result = _main(&args);
    assert_eq!(result, 0, "ls on valid dir should succeed");
}

#[test]
fn test_ls_invalid_dir() {
    let args = ["ls", "doesnotexist"];
    let result = _main(&args);
    assert_eq!(result, 1, "ls on invalid dir should fail");
}