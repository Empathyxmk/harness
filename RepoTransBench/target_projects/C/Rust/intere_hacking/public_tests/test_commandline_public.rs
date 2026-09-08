use std::fs;
use std::io::{BufRead, BufReader};
use std::process::Command;

#[test]
fn test_commandline_public() {
    // Run the commandline binary with a different argument
    let output = Command::new("cargo")
        .args(&["run", "--bin", "commandline", "--", "foo"])
        .output()
        .expect("Failed to execute commandline");
    
    // Check if it ran successfully
    assert!(output.status.success(), "commandline (public) failed to run");
    
    // Check output for expected string
    let output_str = String::from_utf8_lossy(&output.stdout);
    assert!(output_str.contains("foo"), "commandline (public): Output did not match");
    
    println!("commandline (public) ran: PASS");
}