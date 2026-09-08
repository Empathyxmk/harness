use std::fs;
use std::path::Path;
use std::process::Command;
use tree::{walk, Counter};

// Utility to recursively compute expected counts of dirs/files for verification
fn manual_count(dir: &str, n_dir: &mut usize, n_files: &mut usize) {
    let path = Path::new(dir);
    if !path.exists() || !path.is_dir() {
        return;
    }
    
    *n_dir += 1;
    
    if let Ok(entries) = fs::read_dir(path) {
        for entry in entries {
            if let Ok(entry) = entry {
                let path_buf = entry.path();
                let file_name = entry.file_name();
                let file_name_str = file_name.to_string_lossy();
                
                if file_name_str == "." || file_name_str == ".." {
                    continue;
                }
                
                if let Ok(metadata) = fs::metadata(&path_buf) {
                    if metadata.is_dir() {
                        manual_count(&path_buf.to_string_lossy(), n_dir, n_files);
                    } else {
                        *n_files += 1;
                    }
                }
            }
        }
    }
}

#[test]
fn test_walk_basic() {
    // This directory and its contents should exist (created by setup)
    let mut c = Counter::new();
    let res = walk("testdir", "", &mut c);
    
    // Compute expected numbers
    let mut n_dirs = 0;
    let mut n_files = 0;
    manual_count("testdir", &mut n_dirs, &mut n_files);
    
    assert!(res.is_ok());
    assert_eq!(c.dirs, n_dirs);
    assert_eq!(c.files, n_files);
    println!("[PASS] test_walk_basic: dirs={} files={}", c.dirs, c.files);
}

#[test]
fn test_walk_emptydir() {
    let mut c = Counter::new();
    let res = walk("testdir/emptydir", "", &mut c);
    
    assert!(res.is_ok());
    assert_eq!(c.dirs, 1); // just itself
    assert_eq!(c.files, 0);
    println!("[PASS] test_walk_emptydir");
}

#[test]
fn test_walk_permission_denied() {
    // Skip if running as root
    if unsafe { libc::geteuid() } == 0 {
        println!("[SKIP] test_walk_permission_denied (root user)");
        return;
    }
    
    // Set permissions to 0
    assert!(Command::new("chmod")
        .args(&["0", "testdir/noperms"])
        .status()
        .unwrap()
        .success());
    
    let mut c = Counter::new();
    let res = walk("testdir/noperms", "", &mut c);
    
    assert!(res.is_err());
    println!("[PASS] test_walk_permission_denied");
    
    // Restore permissions
    assert!(Command::new("chmod")
        .args(&["0700", "testdir/noperms"])
        .status()
        .unwrap()
        .success());
}

#[test]
fn test_walk_does_not_exist() {
    let mut c = Counter::new();
    let res = walk("testdir/DOESNOTEXIST", "", &mut c);
    
    assert!(res.is_err());
    println!("[PASS] test_walk_does_not_exist");
}

#[test]
fn test_walk_file_instead_of_dir() {
    let mut c = Counter::new();
    let res = walk("testdir/f1.txt", "", &mut c);
    
    assert!(res.is_err()); // can't open as dir
    println!("[PASS] test_walk_file_instead_of_dir");
}