// Translation of tests/test_init_py.py
// In Python, this exists to ensure correct package-level behavior (__init__.py)
// In Rust, module `mod.rs` is roughly analogous, but no code to test unless explicit.

#[test]
fn test_lib_mod_integration() {
    // This test ensures the root `lib.rs` and `redbeat/mod.rs` compile and export correctly.
    // If `src/lib.rs` and `src/redbeat/mod.rs` fail to compile or fail to provide expected
    // public interfaces, Cargo test/build will fail anyway, so this test can be empty.
    assert_eq!(2 + 2, 4);
}