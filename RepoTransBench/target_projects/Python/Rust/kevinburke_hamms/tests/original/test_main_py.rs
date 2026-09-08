#[test]
fn test_main_guard() {
    // Simulate import of main, for coverage
    // Rust doesn't run main() on import, so just "call" the function for test
    let _ = kevinburke_hamms::main_mod::main_output() as &str;
}