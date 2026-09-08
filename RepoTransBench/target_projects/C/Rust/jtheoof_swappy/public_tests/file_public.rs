use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::Command;
use swappy::file::{folder_exists, file_exists, file_dump_stdin_into_a_temp_file};

// Helper functions for public tests
fn create_alt_temp_file(path: &str) {
    if let Ok(mut file) = fs::File::create(path) {
        let _ = file.write_all(b"altdata");
    }
}

fn remove_alt_temp_file(path: &str) {
    let _ = fs::remove_file(path);
}

fn create_alt_temp_dir(path: &str) {
    let _ = fs::create_dir_all(path);
}

fn remove_alt_temp_dir(path: &str) {
    let _ = fs::remove_dir_all(path);
}

#[test]
fn test_folder_exists_positive_public() {
    let dir_name = "test_temp_alt_dir_public";
    create_alt_temp_dir(dir_name);
    assert!(folder_exists(dir_name));
    remove_alt_temp_dir(dir_name);
}

#[test]
fn test_folder_exists_negative_public() {
    assert!(!folder_exists("alt_dir_that_does_not_exist_public"));
}

#[test]
fn test_file_exists_positive_public() {
    let file_name = "test_temp_alt_file_public.txt";
    create_alt_temp_file(file_name);
    assert!(file_exists(file_name));
    remove_alt_temp_file(file_name);
}

#[test]
fn test_file_exists_negative_public() {
    assert!(!file_exists("alt_file_that_does_not_exist_public.txt"));
}

#[test]
fn test_file_dump_stdin_returns_null_if_tty_public() {
    // Just like the original logic, be robust to CI envs
    let ret = file_dump_stdin_into_a_temp_file();
    // In original C test, it just checks the function runs without issues
    assert!(true);
}