use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process::Command;

#[test]
fn test_crypt_test_output() {
    // Run the crypt_test binary
    let status = Command::new("cargo")
        .args(&["run", "--bin", "crypt_test", "--", "password", "xx"])
        .output()
        .expect("Failed to execute crypt_test");
    
    // Check if it ran successfully
    assert!(status.status.success(), "crypt_test failed to run");
    
    // Check output for expected string
    let output = String::from_utf8_lossy(&status.stdout);
    assert!(output.contains("hashes to ==>"), "crypt_test: Output did not match");
    
    println!("crypt_test ran: PASS");
}