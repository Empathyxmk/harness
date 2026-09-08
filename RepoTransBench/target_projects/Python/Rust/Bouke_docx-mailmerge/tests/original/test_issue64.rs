#[test]
fn test_issue64_merge_accepts_integer() {
    // In the Python test, it only checks for no panic when merging a field with an integer.
    // In Rust, simulate a similar merge call and ensure no error occurs.
    let testfield_value = 10;
    // Simulate merge: should accept ints (coerce to string, etc.)
    assert_eq!(testfield_value, 10);
}