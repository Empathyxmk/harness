use std::fs::File;
use std::io::{Write, Read};
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::str;
use tempfile::NamedTempFile;

// Helper function to run map command with input and return output
fn run_map_with_input(input: &str, args: &[&str]) -> String {
    let mut child = Command::new("./target/debug/map")
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("Failed to spawn map process");
    
    if let Some(mut stdin) = child.stdin.take() {
        stdin.write_all(input.as_bytes()).expect("Failed to write to stdin");
    }
    
    let output = child.wait_with_output().expect("Failed to wait on map");
    String::from_utf8_lossy(&output.stdout).to_string()
}

#[test]
fn test_normal_usage_with_one_line_input() {
    // Test: normal usage with one-line input, command using the variable
    assert_eq!("foofoo", run_map_with_input("foo", &["f", "printf $f$f"]));
}

#[test]
fn test_multi_line_input() {
    // Test: multi-line input using input file
    let mut input_content = String::new();
    File::open("tests/data/input")
        .expect("Failed to open input file")
        .read_to_string(&mut input_content)
        .expect("Failed to read input file");
    
    assert_eq!("foobarbaz", run_map_with_input(&input_content, &["f", "printf $f"]));
}

#[test]
fn test_empty_stdin() {
    // Test: edge case: empty stdin (no input, should not call command)
    assert_eq!("", run_map_with_input("", &["VAR", "echo hit"]));
}

#[test]
fn test_single_character_input() {
    // Test: single character input
    assert_eq!("aa", run_map_with_input("a", &["f", "printf $f$f"]));
}

#[test]
fn test_newline_only_input() {
    // Test: input with only a newline
    assert_eq!("", run_map_with_input("\n", &["f", "echo nohit"]));
}

#[test]
fn test_usage_error() {
    // Test: usage error, argc != 3
    let output = Command::new("./target/debug/map")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .expect("Failed to execute map");
    
    let exit_code = output.status.code().unwrap_or(-1);
    let error_output = String::from_utf8_lossy(&output.stderr);
    
    assert_eq!(1, exit_code);
    assert!(error_output.contains("usage: "), "Error message should contain 'usage: '");
}