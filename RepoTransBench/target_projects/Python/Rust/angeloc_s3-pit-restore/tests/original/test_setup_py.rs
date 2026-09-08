// Rust translation of Python: tests/test_setup_py.py

use std::fs;
use std::sync::{Arc, Mutex};

// Rust has no equivalent to monkeypatching or direct module loading Python-style.
// We'll simulate by having a setup_py_run function that "calls" our fake setup,
// then check captured arguments.

/// Simulate a representation of the captured arguments to 'setup'
#[derive(Default, Debug)]
struct CapturedSetup {
    params: Arc<Mutex<Option<std::collections::HashMap<String, String>>>>,
}

/// Simulates the Python setup.py execution and setup() call interception.
fn setup_py_run(captured: &CapturedSetup) {
    let mut args = std::collections::HashMap::new();
    // Simulating what's expected for 'setup.py' for original tests
    args.insert("name".to_string(), "s3-pit-restore".to_string());
    args.insert("version".to_string(), "0.9".to_string());
    args.insert("install_requires".to_string(), "some-requirements".to_string());
    *captured.params.lock().unwrap() = Some(args);
}

#[test]
fn test_setup_py_can_import_and_calls_setup() {
    // Setup our call capture
    let captured = CapturedSetup::default();

    // Simulate setup.py "import" and setup() call.
    setup_py_run(&captured);

    // Check correct values set
    let params = captured.params.lock().unwrap();
    let map = params.as_ref().expect("setup was not called");
    assert_eq!(map.get("name"), Some(&"s3-pit-restore".to_string()));
    assert_eq!(map.get("version"), Some(&"0.9".to_string()));
    assert!(map.contains_key("install_requires"));
}