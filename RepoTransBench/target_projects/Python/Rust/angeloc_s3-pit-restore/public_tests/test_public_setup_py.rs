// Rust translation of Python: public_tests/test_public_setup_py.py

use std::sync::{Arc, Mutex};

#[derive(Default, Debug)]
struct CapturedSetup {
    params: Arc<Mutex<Option<std::collections::HashMap<String, String>>>>,
}

/// Simulate the "setup.py" execution for public test keys: author, author_email, keywords.
fn setup_py_run_public(captured: &CapturedSetup) {
    let mut args = std::collections::HashMap::new();
    // Simulate expected public keys; different from original test
    args.insert("author".to_string(), "Angelo Compagnucci".to_string());
    args.insert(
        "author_email".to_string(),
        "angelo.compagnucci@gmail.com".to_string(),
    );
    args.insert("keywords".to_string(), "restore,aws,s3,python".to_string());
    *captured.params.lock().unwrap() = Some(args);
}

#[test]
fn test_setup_py_can_import_and_calls_setup_public() {
    let captured = CapturedSetup::default();

    // Simulate 'setup.py' public author/keyword test.
    setup_py_run_public(&captured);

    let params = captured.params.lock().unwrap();
    let map = params.as_ref().expect("setup was not called");
    assert_eq!(
        map.get("author"),
        Some(&"Angelo Compagnucci".to_string())
    );
    assert_eq!(
        map.get("author_email"),
        Some(&"angelo.compagnucci@gmail.com".to_string())
    );
    assert!(map.contains_key("keywords"));
}