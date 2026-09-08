use std::fs;
use std::process::Command;

#[test]
fn test_auth_overflow_public() {
    // Run the auth_overflow binary with different inputs
    let output = Command::new("cargo")
        .args(&["run", "--bin", "auth_overflow", "--", "alice", "newpassword"])
        .output()
        .expect("Failed to execute auth_overflow");
    
    // Check if it ran successfully
    assert!(output.status.success(), "auth_overflow (public) failed to run");
    
    // Check that output contains something
    let output_str = String::from_utf8_lossy(&output.stdout);
    assert!(!output_str.is_empty(), "auth_overflow (public): Output did not match");
    
    println!("auth_overflow (public) ran: PASS");
}