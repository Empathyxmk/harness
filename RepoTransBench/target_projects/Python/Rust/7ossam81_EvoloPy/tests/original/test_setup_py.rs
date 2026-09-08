use std::process::Command;
use assert_cmd::Command as AssertCommand;

#[test]
fn test_setup_py_runs() {
    let output = Command::new("cargo")
        .arg("build")
        .output()
        .expect("cargo build failed");
    assert!(output.status.success());
    
    let output_help = Command::new("./target/debug/evolopy_rs")  // Assuming the binary name
        .arg("--help")
        .output()
        .expect("Help command failed");
    let stdout = String::from_utf8_lossy(&output_help.stdout);
    assert!(stdout.contains("help") || stdout.contains("Help"));
}