/// Rust translation of tests/test_examples_scandir.c

use std::fs::{self, File};
use std::io::Write;
use tempfile::tempdir;

use tronkko_dirent_rust::examples::scandir::_main;

#[test]
fn test_scandir_list_current() {
    let args = ["scandir"];
    let result = _main(&args);
    assert_eq!(result, 0, "scandir with no arguments should list dir");
}

#[test]
fn test_scandir_with_pattern() {
    let dir = tempdir().unwrap();
    let testfile = dir.path().join("foo123.txt");
    File::create(&testfile).unwrap();
    let args = ["scandir", "*"];
    let result = _main(&args);
    assert_eq!(result, 0, "scandir pattern '[dir]/*' should succeed");
}

#[test]
fn test_scandir_specific_file() {
    let dir = tempdir().unwrap();
    let testfile = dir.path().join("barfile.txt");
    File::create(&testfile).unwrap();
    let args = ["scandir", testfile.to_str().unwrap()];
    let result = _main(&args);
    assert_eq!(result, 0, "scandir with known file should succeed");
}

#[test]
fn test_scandir_nonexistent() {
    let args = ["scandir", "ZZZ_NON_EXISTENT"];
    let result = _main(&args);
    assert_eq!(result, 1, "scandir should fail for non-existent pattern/dir");
}