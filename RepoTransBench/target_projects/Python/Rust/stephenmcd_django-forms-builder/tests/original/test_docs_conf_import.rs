use std::collections::HashMap;

/// Simulates import and calling of a docs conf setup handler as in Python.
/// Since Rust does not support dynamic code import from files, simply test
/// ability to execute dummy setup logic and set a flag.
#[test]
fn test_docs_conf_import_like() {
    let mut called = HashMap::new();
    // Simulate monkeypatching and module injection
    fn setup_conf(_g: &mut HashMap<&str, bool>) {
        _g.insert("run", true);
    }
    setup_conf(&mut called);
    assert!(called.get("run").is_some());
}