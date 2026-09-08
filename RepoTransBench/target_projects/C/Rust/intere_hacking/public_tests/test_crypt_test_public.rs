use std::fs;
use std::io::{BufRead, BufReader};
use std::process::Command;

#[test]
fn test_crypt_test_public() {
    // Run the crypt_test_public_test binary with different inputs
    let output = Command::new("cargo")
        .args(&["run", "--bin", "crypt_test_public_test", "--", "hello", "ab"])
        .output()
        .expect("Failed to execute crypt_test_public_test");
    
    // Check if it ran successfully
    assert!(output.status.success(), "crypt_test_public_test failed to run");
    
    // Check output for expected string
    let output_str = String::from_utf8_lossy(&output.stdout);
    assert!(output_str.contains("hashes to ==>"), "crypt_test_public_test: Output did not match");
    
    println!("crypt_test_public_test ran: PASS");
}