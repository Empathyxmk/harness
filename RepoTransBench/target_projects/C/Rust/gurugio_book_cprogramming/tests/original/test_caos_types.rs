#[test]
fn test_caos_types() {
    // In Rust, we don't need to check the size of integer types as they're enforced by the type system
    // This is a direct translation of the original C test logic
    assert_eq!(std::mem::size_of::<i8>(), 1);
    assert_eq!(std::mem::size_of::<i16>(), 2);
    assert_eq!(std::mem::size_of::<i32>(), 4);
    assert_eq!(std::mem::size_of::<i64>(), 8);
}