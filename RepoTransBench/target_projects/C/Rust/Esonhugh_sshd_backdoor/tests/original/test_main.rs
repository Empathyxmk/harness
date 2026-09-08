//! Translated from test/fake_sshd/test_main.c

use std::fs::{File, OpenOptions, remove_file, create_dir_all};
use std::io::{Read, Write};
use std::os::unix::fs::OpenOptionsExt;
use std::os::unix::io::AsRawFd;
use std::path::Path;
use std::ffi::CString;
use libc::{open, close, read, O_RDONLY};
use std::ptr;
use std::io;
use std::fs;
use tempfile::TempDir;

// Helper: Safe unlink, ignore errors if file is missing
fn safe_unlink(path: &str) {
    let _ = remove_file(path);
}

// Test opening and reading the authorized_keys file exists
#[test]
fn test_read_authorized_keys() {
    let ssh_dir = "/root/.ssh";
    let filepath = "/root/.ssh/authorized_keys";
    // Prepare file
    let _ = create_dir_all(ssh_dir);
    let mut f = File::create(filepath).expect("couldn't create file");
    f.write_all(b"unit-test-key").expect("couldn't write test key");
    f.sync_all().unwrap();

    // Open file
    let c_file = CString::new(filepath).unwrap();
    unsafe {
        let fd = open(c_file.as_ptr(), O_RDONLY);
        assert!(fd >= 0, "File should be openable");

        let mut buf = [0u8; 4096];
        let n = read(fd, buf.as_mut_ptr() as *mut _, 4096);
        assert!(n > 0, "Should read >0 bytes from file");
        let s = std::str::from_utf8(&buf[0..n as usize]).expect("Valid UTF8 expected");
        assert!(s.contains("unit-test-key"), "File contains test key");

        close(fd);
    }

    println!("test_read_authorized_keys passed");
    safe_unlink(filepath);
}

#[test]
fn test_file_not_found() {
    let filepath = "/root/.ssh/authorized_keys";
    safe_unlink(filepath);

    let c_file = CString::new(filepath).unwrap();
    unsafe {
        let fd = open(c_file.as_ptr(), O_RDONLY);
        assert!(fd < 0, "Should not open non-existent file");
        // Do not call read if fd<0, test code should act accordingly - simulate
    }
    println!("test_file_not_found passed");
}

#[test]
fn test_empty_file() {
    let ssh_dir = "/root/.ssh";
    let filepath = "/root/.ssh/authorized_keys";
    let _ = create_dir_all(ssh_dir);
    File::create(filepath).expect("failed to create empty file");

    let c_file = CString::new(filepath).unwrap();
    unsafe {
        let fd = open(c_file.as_ptr(), O_RDONLY);
        assert!(fd >= 0, "Should be able to open empty file");

        let mut buf = [0u8; 4096];
        let n = read(fd, buf.as_mut_ptr() as *mut _, 4096);
        assert_eq!(n, 0, "Nothing to read for empty file");

        close(fd);
    }
    println!("test_empty_file passed");
    safe_unlink(filepath);
}

#[test]
fn test_large_file() {
    let ssh_dir = "/root/.ssh";
    let filepath = "/root/.ssh/authorized_keys";
    let _ = create_dir_all(ssh_dir);
    let mut f = File::create(filepath).expect("couldn't create file");
    // Write 4096 bytes
    for i in 0..4096 {
        let ch = b'A' + (i % 26) as u8;
        f.write_all(&[ch]).unwrap();
    }
    f.sync_all().unwrap();

    let c_file = CString::new(filepath).unwrap();
    unsafe {
        let fd = open(c_file.as_ptr(), O_RDONLY);
        assert!(fd >= 0, "Large file should be openable");

        let mut buf = [0u8; 4097];
        let n = read(fd, buf.as_mut_ptr() as *mut _, 4096);
        assert_eq!(n, 4096, "Should read 4096 bytes");

        close(fd);
    }
    println!("test_large_file passed");
    safe_unlink(filepath);
}