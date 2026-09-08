#[test]
fn test_import_hamms_main() {
    // "Import" the module by referencing the function and ensure it compiles
    let _ = kevinburke_hamms::main_mod::main_output() as &str;
}

#[test]
fn test_main_function_captures_output() {
    // Simulate calling main() and capturing output
    use std::io::{self, Write};
    let output = kevinburke_hamms::main_mod::main_output();
    assert!(output.contains("hamms main executed"));
}