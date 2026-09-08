//! Translated from test/fake_sshd/test_main_public.c

use std::fs::{File, OpenOptions};
use std::os::unix::fs::OpenOptionsExt;
use std::io::Write;
use std::os::unix::io::AsRawFd;
use std::ffi::CString;
use libc::{open, close, read, O_RDONLY};
use std::fs::create_dir_all;

// Technically, not #[test] per function but combine as translation of main
#[test]
fn test_public_read_logic() {
    let pub_path = "/root/.ssh/public_authorized_keys";
    let pub_expected = b"public-dummy-key\nsecond-public-key\n";

    // Prepare file to match the C test expectations
    let _ = create_dir_all("/root/.ssh");
    let mut f = File::create(pub_path).expect("cannot create public_authorized_keys");
    f.write_all(pub_expected).expect("cannot write test keys");
    f.sync_all().unwrap();

    // test_read_public_keys
    let c_filename = CString::new(pub_path).unwrap();
    let mut buf = [0u8; 4096];
    let sz = unsafe {
        let fd = open(c_filename.as_ptr(), O_RDONLY);
        assert!(
            fd >= 0,
            "test_read_public_keys: FAIL (cannot open file)"
        );
        let read_sz = read(fd, buf.as_mut_ptr() as *mut _, buf.len());
        close(fd);
        assert!(
            read_sz > 0,
            "test_read_public_keys: FAIL (could not read file)"
        );
        read_sz
    };
    let s = std::str::from_utf8(&buf[0..sz as usize]).expect("UTF-8 expected");
    assert!(
        s.contains("public-dummy-key") && s.contains("second-public-key"),
        "test_read_public_keys: FAIL (expected test data not found)"
    );
    println!("test_read_public_keys: PASS");

    // test_nonexistent_file
    let missing_path = "/root/.ssh/nonexistent_public_file";
    let c_missing = CString::new(missing_path).unwrap();
    let fd = unsafe { open(c_missing.as_ptr(), O_RDONLY) };
    if fd >= 0 {
        // If the file exists (shouldn't), close and fail
        unsafe { close(fd) };
    }
    assert!(
        fd < 0,
        "test_nonexistent_file: FAIL (file unexpectedly exists)"
    );
    println!("test_nonexistent_file: PASS");
}