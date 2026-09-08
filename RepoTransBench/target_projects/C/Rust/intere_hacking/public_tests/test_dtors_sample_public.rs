use std::fs;
use std::io::{BufRead, BufReader};
use std::process::Command;

#[test]
fn test_dtors_sample_public() {
    // Run the dtors_sample binary
    let output = Command::new("cargo")
        .args(&["run", "--bin", "dtors_sample"])
        .output()
        .expect("Failed to execute dtors_sample");
    
    // Check if it ran successfully
    assert!(output.status.success(), "dtors_sample (public) failed to run");
    
    // Check output for expected strings
    let output_str = String::from_utf8_lossy(&output.stdout);
    let mainmsg = output_str.contains("Some actions happen in the main");
    let destructormsg = output_str.contains("In the cleanup function now");
    
    assert!(mainmsg && destructormsg, "dtors_sample (public): Output did not match");
    
    println!("dtors_sample (public) ran: PASS");
}