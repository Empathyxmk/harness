#[test]
fn test_public_setup_py_still_runs() {
    // Run `python3 setup.py` (simulate)
    let output = std::process::Command::new("python3")
        .arg("setup.py")
        .output()
        .expect("failed to run setup.py");
    assert!(output.status.success());
}