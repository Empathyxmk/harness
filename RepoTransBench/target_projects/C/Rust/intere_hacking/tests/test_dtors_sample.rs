use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process::Command;

#[test]
fn test_dtors_sample_output() {
    // Run the dtors_sample binary
    let status = Command::new("cargo")
        .args(&["run", "--bin", "dtors_sample"])
        .output()
        .expect("Failed to execute dtors_sample");
    
    // Check if it ran successfully
    assert!(status.status.success(), "dtors_sample did not exit cleanly");
    
    // Check output for expected strings
    let output = String::from_utf8_lossy(&status.stdout);
    let found_main = output.contains("main() function");
    let found_cleanup = output.contains("cleanup function");
    
    assert!(found_main && found_cleanup, "dtors_sample output missing main/cleanup");
    
    println!("dtors_sample test: PASS");
}