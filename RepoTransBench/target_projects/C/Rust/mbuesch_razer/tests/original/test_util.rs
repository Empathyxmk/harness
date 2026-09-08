fn test_dummy() -> i32 {
    // Placeholder to ensure the test runs
    42
}

#[test]
fn test_util() {
    assert_eq!(test_dummy(), 42);
    println!("test_util passed");
}