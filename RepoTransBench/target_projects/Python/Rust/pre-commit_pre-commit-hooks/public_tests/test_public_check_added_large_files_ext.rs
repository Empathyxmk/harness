// This is a translation of the public Python tests for checking large files

use tempfile::TempDir;
use std::fs;

#[test]
fn test_public_small_file() {
    let dir = TempDir::new().unwrap();
    let file = dir.path().join("foo.bin");
    fs::write(&file, vec![b'x'; 1024]).unwrap();
    assert_eq!(check_added_large_files_main(&[file.to_str().unwrap()]), 0);
}

#[test]
fn test_public_big_file() {
    let dir = TempDir::new().unwrap();
    let file = dir.path().join("large.txt");
    fs::write(&file, vec![b'y'; 900 * 1024]).unwrap();
    // override limit to smaller to force failure
    assert_eq!(
        check_added_large_files_main_with_maxkb(100, &[file.to_str().unwrap()]),
        1
    );
}

#[test]
fn test_public_exact_limit() {
    let dir = TempDir::new().unwrap();
    let file = dir.path().join("some.txt");
    fs::write(&file, vec![b'z'; 400 * 1024]).unwrap();
    assert_eq!(
        check_added_large_files_main_with_maxkb(400, &[file.to_str().unwrap()]),
        0
    );
}

// These are stub functions. Implement logic or link to your implementation.
fn check_added_large_files_main(_files: &[&str]) -> i32 { 0 }
fn check_added_large_files_main_with_maxkb(_maxkb: u64, _files: &[&str]) -> i32 { 0 }